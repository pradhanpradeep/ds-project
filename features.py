import os
import numpy as np
import pymongo
import traceback

from pymongo import Connection
from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import date, datetime, timedelta

from utils import print_time, load_features, load_sentiment_scores, pickle_features

data_dir = os.getcwd() + "/data"


def get_features(limit=1000, features=[], stemmer_type="RegexpStemmer", db_name="yelp_train", standardized=False):
    """
    -----------------------------------------------
    It does a bit of optimization
    Loads features from pickle, if the features with
    the specified input conditions are already pickled
    
    If not fetches from the database (MongoDB)
    -----------------------------------------------
    """
    if os.path.exists(data_dir + "/X_%s_%s_%s_%s.pickle"%(limit, db_name, stemmer_type, "-".join(features))):
        X = load_features("X_%s_%s_%s_%s.pickle"%(limit, db_name, stemmer_type, "-".join(features)))
        y = load_features("Y_%s_%s_%s_%s.pickle"%(limit, db_name, stemmer_type, "-".join(features)))
        z = load_features("Z_%s_%s_%s_%s.pickle"%(limit, db_name, stemmer_type, "-".join(features)))
        
    else:
        #! fetch features from database
        X, y, z = extract_and_save_features(limit=limit, features=features, stemmer_type=stemmer_type, db_name=db_name, standardized=standardized)
        
    return X, y, z



def standardize(data):
    """
    --------------------------------------
    Standardize quantitative data array
    --------------------------------------
    """
    scaler = preprocessing.StandardScaler()
    return scaler.fit_transform(data)
    #return preprocessing.scale(data)



def extract_and_save_features(limit=1000, features=[], stemmer_type=None, db_name="yelp_train", standardized=False):
    """
    --------------------------------------
     Fetch features from database
    --------------------------------------
    """
    sentiment_dict = {}
    if stemmer_type and db_name == "yelp_train":
        sentiment_dict = load_sentiment_scores('review_training_sentiment_scores_%s.csv' %(stemmer_type))
    elif stemmer_type and db_name == "yelp_test":
        sentiment_dict = load_sentiment_scores('review_test_sentiment_scores_%s.csv' %(stemmer_type))

    X = [] #! response variables
    y = [] #! target variables
    z = [] #! list of review_ids used for mapping when predicting
    
    connection = Connection() ##('localhost', 27017) #! get connection
    db = connection[db_name] #! get database
    collection = db["review"]

    if int(limit) == 0:
        reviews = collection.find().batch_size(1000) #! grab all records from the db
    else:
        reviews = collection.find(limit=limit).batch_size(1000)

    #! get the other dataset cursors        
    collection_user = db["user"]
    collection_busi = db["business"]
    collection_check = db['checkin']    
    
    if db_name == "yelp_train":
        review_cutoff = datetime(2013, 01, 19, 0, 0, 0)
    elif db_name == "yelp_test":
        review_cutoff = datetime(2013, 03, 12, 0, 0, 0)
    else:
        #! this case shouldn't arise
        return X, y, z
        
    for review in reviews:
        temp = []        
        z.append(review['review_id']) 
        
        temp.append(len(review['text']))
        review_age = (review_cutoff - datetime.strptime(review['date'], "%Y-%m-%d")).days
        temp.append(review_age)
        
        #! ---------------------------------------------
        if 'votes' in features:
            try:
                daily_avg_useful_votes = review['votes']['useful'] / review_age                
                temp.append(daily_avg_useful_votes)
            except:
                temp.append(0)
            
        try:
            #! -------------------------------------------
            #! Business features
            if 'business' in features:
                business = None
                try:
                    business = collection_busi.find_one({'business_id':review['business_id']})
                    temp.append(business['review_count'])
                except:
                    temp.append(0)
                
                try:
                    temp.append(business['stars'])
                except:
                    temp.append(0)

            #! ---------------------------------------------
            #! Checkin features
            if 'checkin' in features:
                try:
                    checkin = collection_check.find_one({'business_id':review['business_id']})
                    #! sum of checkins for this business
                    checkin_total = np.sum([int(item) for item in checkin['checkin_info'].values()])
                    temp.append(checkin_total)
                except:
                    temp.append(0)

            #! ---------------------------------------------
            #! User features
            user = None
            if 'user' in features:
                try:
                    user = collection_user.find_one({'user_id':review['user_id']})                    
                    temp.append(user['review_count'])
                    temp.append(user['average_stars'])
                except:
                    temp.append(0)
                    temp.append(0)
                    

            if 'user' and 'votes' in features:
                try:
                    temp.append(user['votes']['useful'] / user['review_count'])
                except:
                    temp.append(0)
                    
            #! ---------------------------------------------
            #! sentiment score
            if stemmer_type:
                temp.append(int(sentiment_dict[review['review_id']]))

            #! ---------------------------------------------
            #! y - useful votes
            try:
                y.append(review['votes']['useful'])
            except Exception, e:
                y.append(0) #! this is in case of test data

            X.append(temp)
        except Exception, e:
            print traceback.format_exc(), review['review_id'], review['user_id']
            continue        

    X = np.array(X).astype(np.float32)
    y = np.array(y).astype(np.float32)
    
    if standardized:
        X = standardize(X)
        y = standardize(y)
    
    #print len(X), '---'
    #print len(y), '---'
    
    #! save extracted features as pickles
    pickle_features("X_%i_%s_%s_%s.pickle"%(limit, db_name, stemmer_type, "-".join(features)), X)
    pickle_features("Y_%i_%s_%s_%s.pickle"%(limit, db_name, stemmer_type, "-".join(features)), y)
    pickle_features("Z_%i_%s_%s_%s.pickle"%(limit, db_name, stemmer_type, "-".join(features)), z)
    
    return X, y, z



def vectorize(limit=1000):
    """
    -----------------------------------------------
    Tried a bit of TFIDF vectorizing
    But couldn't finish due to system contraints
    -----------------------------------------------
    """
    connection = Connection() ##('localhost', 27017) #! get connection
    db = connection['yelp'] #! get database
    collection = db["review"]
    collection_busi = db["business"].find()
    collection_user = db["user"].find()
    
    busi_ids = [item['business_id'] for item in collection_busi]
    user_ids = [user['user_id'] for user in collection_user]
    print len(busi_ids)
    if int(limit) == 0:
        reviews = collection.find({"business_id" :{"$in" : busi_ids}, "user_id" :{"$in" : user_ids}}) #! grab all records from the db
    else:
        reviews = collection.find({"business_id" :{"$in" : busi_ids}, "user_id" :{"$in" : user_ids}}, limit=limit)

    corpus = []
    y = []
    for review in reviews:
        try:            
            corpus.append(review['text'])
            y.append(review['votes']['useful'])
        except:
            continue
        
    vectorizer = TfidfVectorizer(min_df=0.1, ngram_range=(1, 2),
                                 stop_words='english', analyzer='word')    
    X = vectorizer.fit_transform(corpus)
    m,n = X.shape
    print m, n
    
    X = X.toarray()
    y = np.array(y).astype(np.float64)
    return X, y



if __name__ == '__main__':
    #vectorize(limit=1000)
    pass
    
    