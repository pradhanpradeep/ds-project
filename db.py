import sys
import os
import json
import traceback
import pymongo
from pymongo import Connection
from pymongo import ASCENDING, DESCENDING

from utils import print_time

@print_time
def load_json(filename='', db_name='', collection_name='', clean=False):
    """
    -------------------------
    load data into Mongo db
    -------------------------
    """
    connection = Connection() ##('localhost', 27017) #! get connection
    db = connection[db_name] #! get database
    collection = db[collection_name] #! get collection
    if clean:
    	collection.remove() # 

    count = 0
    with open(filename, 'rb') as input_file:
        for idx, line in enumerate(input_file):
            line = line.strip('\r\n').strip('\n')
            json_obj = json.loads(line, encoding="utf-8")
            try:
                collection.insert(json_obj)
                count += 1
            except:
                print traceback.format_exc()
                break

    connection.close()
    print '------------- total json objects found = %s --- ' % (idx+1)
    print '------------- total json objects loaded = %s --- ' % (count)

if __name__ == "__main__":
    curr_dir = os.getcwd()
    load_json(filename=curr_dir + '/data/yelp_training_set_review.json', db_name='yelp_train', collection_name='review', clean=True)
    load_json(filename=curr_dir + '/data/yelp_test_set_review.json', db_name='yelp_test', collection_name='review', clean=True)

    load_json(filename=curr_dir + '/data/yelp_training_set_business.json', db_name='yelp_train', collection_name='business', clean=True)
    load_json(filename=curr_dir + '/data/yelp_test_set_business.json', db_name='yelp_test', collection_name='business', clean=True)

    load_json(filename=curr_dir + '/data/yelp_training_set_user.json', db_name='yelp_train', collection_name='user', clean=True)
    load_json(filename=curr_dir + '/data/yelp_test_set_user.json', db_name='yelp_test', collection_name='user', clean=True)

    load_json(filename=curr_dir + '/data/yelp_training_set_checkin.json', db_name='yelp_train', collection_name='checkin', clean=True)
    load_json(filename=curr_dir + '/data/yelp_test_set_checkin.json', db_name='yelp_test', collection_name='checkin', clean=True)