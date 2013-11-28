import os
import sys
import nltk
#nltk.download()

from nltk import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import RegexpStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import csv
import re
import json
import time

import pymongo
from pymongo import Connection
from pymongo import ASCENDING, DESCENDING

def print_time(func):
    """
    -------------------------------------------------------------------
    This is a simple decorator function to print the start and end time
      of a function it decorates.
    -------------------------------------------------------------------
    """
    def wrapper_func(*args):
        print '------- start time - (%s) -----'%(time.asctime())
        func(*args)
        print '------- finish time - (%s) -----'%(time.asctime())
    return wrapper_func

def preprocess_pipeline(str, lang="english", stemmer_type="PorterStemmer", return_as_str=False,
                        do_remove_stopwords=False, do_clean_html=False):
    l = []
    words = []
    if do_clean_html:
        sentences = tokenize(html2text(str))
    else:
        sentences = tokenize(str)
    for sentence in sentences:
        if do_remove_stopwords:
            words = remove_stopwords(sentence, lang)
        else:
            words = sentence
        words = stemming(words, stemmer_type)
        if return_as_str:
            l.append(" ".join(words))
        else:
            l.append(words)
    if return_as_str:
        return " ".join(l)
    else:
        return l

def remove_stopwords(word_list):
    filtered_word_list = word_list[:] #make a copy of the word_list
    for word in word_list: # iterate over word_list
        if word in stopwords.words('english'): 
            filtered_word_list.remove(word)
    return filtered_word_list

def stemming(word_list, stemmer_type="PorterStemmer"):
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
def calculate_sentiment_score():
    print '==============================='
    sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')

    sent_file = open("examples/AFINN/AFINN-111.txt", 'rb')
    word_scores_data = list(csv.reader(sent_file, delimiter="\t"))
    word_scores_dict = dict([(k,int(v)) for k,v in word_scores_data])
    for key in word_scores_dict: print key, word_scores_dict[key];break
    sent_file.close()

    print word_scores_data[0]

    out_f = open('data/review_sentiment_scores.csv', 'wb')
    with open('yelp_training_set/yelp_training_set_review.json', 'rb') as input_file:
        for idx, line in enumerate(input_file):
            line = line.strip('\r\n').strip('\n')
            json_obj = json.loads(line, encoding="utf-8")
            #print json_obj.keys()

            #print '==============================='
            review = json_obj['text']
            sents = sent_tokenizer.tokenize(review)
            #print sents

            #print '==============================='
            refined = []
            for sent in sents:
                #print nltk.word_tokenize(sent)
                words = remove_stopwords(nltk.word_tokenize(sent))
                #print words, ' *** without stop words'
                porter_stem = stemming(words, stemmer_type="PorterStemmer")
                #print porter_stem, ' *** Porter Stemmer'
                refined.extend(porter_stem)
                #lancaster_stem = stemming(words, stemmer_type="LancasterStemmer")
                #print lancaster_stem, ' *** Lancaster Stemmer'
                #regx_stem = stemming(words, stemmer_type="RegexpStemmer")
                #print regx_stem, ' *** RegexpStemmer'
                #print '---------'
            score = 0
            for word in refined:
                try:
                    score += word_scores_dict[word]
                    #print score
                except:
                    continue
            csv.writer(out_f).writerow([json_obj['review_id'], score])
            #if idx > 20: break
            #prep = preprocess_pipeline(json_obj['text'])
            #print prep
    out_f.close()


if __name__ == "__main__":
    #data_dir = os.getcwd()
    #load_json(filename=data_dir + '/data/yelp_training_set_review.json' , collection_name='business')
    calculate_sentiment_score()
            