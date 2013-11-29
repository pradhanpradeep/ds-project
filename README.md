welcome to ds-project
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
      
      *** can ignore this step,if nltk data is not available, I would make sure to copy these across

      the script if executes successfully produces the following output      
      - data/review_test_sentiment_scores_PorterStemmer.csv
      - data/review_test_sentiment_scores_LancasterStemmeStemmer.csv
      - data/review_test_sentiment_scores_RegexpStemmer.csv
      
      - data/review_training_sentiment_scores_PorterStemmer.csv
      - data/review_training_sentiment_scores_LancasterStemmeStemmer.csv
      - data/review_training_sentiment_scores_RegexpStemmer.csv
      
      
4) we are now ready to go, just run main.py script with the default settings.

   all it takes few keyword arguments that need to be passed to models.train() function.
     
     -----------------------------------------------------
     regressors = ['Ridge', 'RandomForestRegressor', 'GradientBoostingRegressor'] #! see config.py 
     features = ['user', 'business', 'checkin', 'votes']

     models.train(modelnames=regressors, features=features, limit=2000, stemmer_type="RegexpStemmer",
                 standardized=False, predict=True, plot=True)
     ------------------------------------------------------

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
                
    - if standardized is set to True, the X and Y arrays are standardized 
      by the sklearn.preprocessing scaling. somehow this wasn't much useful
      in my case.
      
    - if predict is set to True, the predictions on test set
       would be saved as csv in predictions directory

    - if plot is set to True, a graph is drawn with RMSLE
      values at the end of cross validation loop.
                      
    the regressors used in this exercise have been defined in the model_config
    dictionary (config.py) with base parameters.the essence of this config dict is it
    makes easy to tweak the hyper paramerters as required.

    The results on the terminal when the script finishes execution
    should be something similar to listing below:
    
    ------- start time - (Thu Nov 28 17:56:34 2013) -----
    Ridge(alpha=0.25, copy_X=True, fit_intercept=True, max_iter=None,
    normalize=False, solver=auto, tol=0.001)
    ------------------ Cross Validation using Ridge model --------------------
    (fold 1 of 5) MSE : 1.125277 | RMSE: 1.060791 | RMSLE: 0.557563
    (fold 2 of 5) MSE : 1.051657 | RMSE: 1.025503 | RMSLE: 0.566605
    (fold 3 of 5) MSE : 1.001438 | RMSE: 1.000719 | RMSLE: 0.506445
    (fold 4 of 5) MSE : 1.001594 | RMSE: 1.000797 | RMSLE: 0.526186
    (fold 5 of 5) MSE : 1.028208 | RMSE: 1.014006 | RMSLE: 0.593110
    >>> Mean MSE: 1.041635 | Mean RMSE: 1.020363 | Mean RMSLE: 0.549982 <<<
    ------- finish time - (Thu Nov 28 18:00:49 2013) -----
    ====== predicting ......
    ====== predicting done ......

5) rscript.r has few R snippets which I used to produce plots.

6) presentation/business.html (business presentation)

7) presentation/technical.html (technical presentation)

8) docs/ directory has pdf versions

9) png/ directory is for plot images

10) results.log where i was dumping all my terminal outputs

=============
