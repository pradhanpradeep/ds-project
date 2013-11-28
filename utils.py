import time
import os
import cPickle
import csv
import numpy as np

data_dir = os.getcwd() + "/data"
preds_dir = os.getcwd() + "/predictions"

def print_time(func):
    """
    -------------------------------------------------------------------
    This is a simple decorator function to print the start and end time
      of a function it decorates.
    -------------------------------------------------------------------
    """
    def wrapper_func(*args, **kwargs):
        print '------- start time - (%s) -----'%(time.asctime())
        func(*args, **kwargs)
        print '------- finish time - (%s) -----'%(time.asctime())
    return wrapper_func


def load_features(filename):
    """
    ---------------------------------------
     Load features from pickle files
    ---------------------------------------
    """
    f = open(data_dir +"/"+filename, "rb")
    data = cPickle.load(f)
    f.close()
    return data

def pickle_features(filename, data):
    """
    ---------------------------------------
     Dump features to pickle files
    ---------------------------------------
    """	
    f = open(data_dir +"/"+ filename, "wb")
    cPickle.dump(data,f)
    f.close()


def load_sentiment_scores(filename):
    """
    --------------------------------------
     load pre-calculated sentiment scores
    --------------------------------------
    """
    f = open(data_dir +"/"+  filename, 'rb')    
    data = np.array(list(csv.reader(f)))
    f.close()    
    return dict(data)

def save_predictions(data, filename):
    """
    --------------------
     Save predictions
    --------------------
    """	
    f = open(preds_dir +"/"+ filename, "wb")
    csv.writer(f).writerows(data)
    f.close()