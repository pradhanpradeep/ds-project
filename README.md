=========
== welcome to ds-project
==========
Here are the list of steps that would go in testing this code

1) download the data from Kaggle's website
   and extract the contents of train and
   test set in data directory
   
   http://www.kaggle.com/c/yelp-recruiting/data

2) start a local mongodb instance

3) run these scripts in sequence, only once for the first time

   a) python db.py
      (loads dataset into db)

   b) python csvconverter.py
      (csvs required by R and for sentiment scoring)
   
   c) python sentiment_analysis.py
      (calculates sentiment scores and puts the results in data directory.
      this bit requires few pickles to be downloaded from nltk data
      repository)
      
      *** can ignore this step, I would make sure to copy these across

      the script produces the following output      
      - data/review_test_sentiment_scores_PorterStemmer.csv
      - data/review_test_sentiment_scores_LancasterStemmeStemmer.csv
      - data/review_test_sentiment_scores_RegexpStemmer.csv
      
      - data/review_training_sentiment_scores_PorterStemmer.csv
      - data/review_training_sentiment_scores_LancasterStemmeStemmer.csv
      - data/review_training_sentiment_scores_RegexpStemmer.csv
      
      
4) run this script with the default settings.

   all it takes few keyword arguments that can be
   tweaked while calling models.train() function.

    - modelnames is a list with the names configured in
       config.py that we wanna train on

    - features is a list of dataset names from which
       the features are extracted. at the moment it takes
       only numericals and pretty much hardcoded in features.py

    - limit is the number of records (reviews) to be selected
       from database. if set to 'zero', grabs complete dataset 

    - stemmer_type parameter specifies which sentiment score to
       be considered while selecting from a pre-calculated csv
       file.there are possibly four options
       
            . PorterStemmer
            . LancasterStemmer
            . RegexpStemmer
            . None
                   
    - if predict is set to True, the predictions on test set
       would be saved as csv in predictions directory

    - if plot is set to True, a graph is drawn with RMSLE
      values at the end of cross validation loop.
                      
    the regressors used in this exercise
    have been defined in the model_config
    dictionary (models.py) with base
    parameters.
    the essence of this config dict is it
    makes easy to add the required hyper
    paramerters as required.

=============
