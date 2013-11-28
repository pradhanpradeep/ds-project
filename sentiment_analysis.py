import os
import sys
import nltk
from nltk import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import RegexpStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from utils import print_time

import csv
import re
import json

data_dir = os.getcwd() + "/data"

def remove_stopwords(word_list):
    """
    -------------------------
    remove stop words
    -------------------------
    """    
    filtered_word_list = word_list[:] #make a copy of the word_list
    for word in word_list: # iterate over word_list
        if word in stopwords.words('english'): 
            filtered_word_list.remove(word)
    return filtered_word_list

def stemming(word_list, stemmer_type="PorterStemmer"):
    """
    -------------------------
    Returns stemmed words

    A processing interface for removing morphological affixes from words. 
    This process is known as stemming.
    -------------------------
    """
    stemmed_words = []
    stemmer = None
    if stemmer_type == 'PorterStemmer':
        stemmer=PorterStemmer()
    elif stemmer_type == 'LancasterStemmer':
        stemmer = LancasterStemmer()
    elif stemmer_type == 'RegexpStemmer':
        stemmer = RegexpStemmer('ing$|s$|e$', min=3)

    for word in word_list:
        stemmed_words.append(stemmer.stem(word))
    return stemmed_words


@print_time
def calculate_sentiment_score(stemmer_type="PorterStemmer", data_type="training"):
    """
    ------------------------------------------
    a) for each review text, it does stemming
    b) calculates sentiment score

    AFINN dictionary source
    http://www2.imm.dtu.dk/pubdb/views/publication_details.php?id=6010
    ------------------------------------------
    """    
    sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')

    sent_file = open("AFINN/AFINN-111.txt", 'rb')
    word_scores_data = list(csv.reader(sent_file, delimiter="\t"))
    word_scores_dict = dict([(k,int(v)) for k,v in word_scores_data])
    for key in word_scores_dict: print key, word_scores_dict[key];break
    sent_file.close()

    out_f = open(data_dir + '/review_%s_sentiment_scores_%s.csv'%(data_type, stemmer_type), 'wb')
    with open(data_dir + '/yelp_%s_set_review.json'%(data_type), 'rb') as input_file:
        for idx, line in enumerate(input_file):
            line = line.strip('\r\n').strip('\n')
            json_obj = json.loads(line, encoding="utf-8")

            #print '==============================='
            review = json_obj['text']
            sents = sent_tokenizer.tokenize(review)
            #print '==============================='
            refined = []
            for sent in sents:                
                words = remove_stopwords(nltk.word_tokenize(sent))                
                stemmed = stemming(words, stemmer_type=stemmer_type)
                refined.extend(stemmed)
            score = 0
            for word in refined:
                try:
                    score += word_scores_dict[word]
                except:
                    continue
            csv.writer(out_f).writerow([json_obj['review_id'], score])
    out_f.close()


if __name__ == "__main__":
    calculate_sentiment_score(stemmer_type="PorterStemmer", data_type="training")
    calculate_sentiment_score(stemmer_type="LancasterStemmer", data_type="training")
    calculate_sentiment_score(stemmer_type="RegexpStemmer", data_type="training")
    
    calculate_sentiment_score(stemmer_type="PorterStemmer", data_type="test")
    calculate_sentiment_score(stemmer_type="LancasterStemmer", data_type="test")
    calculate_sentiment_score(stemmer_type="RegexpStemmer", data_type="test")
            