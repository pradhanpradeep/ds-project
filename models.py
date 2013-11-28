from sklearn.pipeline import Pipeline
from sklearn import metrics, cross_validation, linear_model, ensemble
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn.grid_search import GridSearchCV
from datetime import date, datetime, timedelta

import numpy as np
import traceback
import gc
import os
import error
import time

#! from local repo
from utils import print_time, save_predictions
from features import get_features, vectorize
from plots import plot_error
from config import model_config

def grid_search(X, y, clf, parameters={}):
	"""
	-----------------------
	grid search
	-----------------------
	"""
	model = GridSearchCV(clf, parameters, cv=3)
	
	

def predict_and_save(X, y, z, test, clf, features):
	"""
	----------------
	fit and predict
	----------------
	"""
	clf.fit(X,y)
	model_name = str(clf.__class__).split(".")[-1].split("'")[0]
	
	#! make predictions on test data and store the results as csv	
	preds = [x for x in clf.predict(test)]
	
	header = [['id', 'votes']]
	result = [[z[index], prediction] for index, prediction in enumerate(preds)]
	
	save_predictions(header + result, model_name + "_Submission_%s_%s-%s.csv"% ("-".join(features),
																				str(date.today()), str(int(time.time()))))



def pipeline(names=[], limit=0):
    """
    -----------------------
    chain estimators
    -----------------------
    """
    #X, y = get_features(limit=limit)
    X, y = vectorize(limit=limit)
    estimators = []
    for name in names:
        model = filter(lambda x: x['name'] == name, model_config)[0]
        
        module_ = __import__(model['module'], fromlist=model['from'])
        class_ = getattr(module_, model['name'])
        clf = class_(**model['kwargs'])
        estimators.append((name, clf))
    
    clf = Pipeline(estimators)
    print clf
    cross_validate(X,y,clf,folds=5,model_name=str(clf.__class__).split(".")[-1].split("'")[0])



def train(modelnames=[], features=[], limit=0, stemmer_type=None, predict=False, standardized=False, plot=False):
	"""
	----------------------------------------
	train - cross validate - predict - plot
	----------------------------------------
	"""
	X, y, z = get_features(limit=limit, features=features, stemmer_type=stemmer_type, db_name="yelp_train", standardized=False)
	del z #! not used when training
	
	for name in modelnames:
		model = filter(lambda x: x['name'] == name, model_config)[0]
		
		#! ---------------------
		module_ = __import__(model['module'], fromlist=model['from'])
		class_ = getattr(module_, model['name'])
		clf = class_(**model['kwargs'])
		model_name = str(clf.__class__).split(".")[-1].split("'")[0]
		
		print clf
		cross_validate(X,y,clf,folds=5,model_name=model_name,plot=plot)
								
		if model['feature_imp']:
			print 'Feature Importances =======', list(clf.feature_importances_)
		gc.collect()
	
		if predict:
			print '====== predicting ......'
			#! grab the complete test set for prediction
			Xtest, ytest, ztest = get_features(limit=0, features=features, stemmer_type=stemmer_type, db_name="yelp_test", standardized=False)
			predict_and_save(X, y, ztest, Xtest, clf, features)
			print '====== predicting done ......'



def cross_validate(X,y,model,folds=5,random_seed=42,test_size=.2,model_name='',parameters={},plot=False):
	"""
	-----------------------
	cross validate models
	-----------------------
	"""
	print ' ------------------ Cross Validation using %s model -------------------- '% model_name
	mses=[];rmses=[];rmsles=[]
	
	for fold in range(folds):		
		#! create a test and train cv set
		train_cv, test_cv, y_target, y_true = cross_validation.train_test_split(X, y, test_size=test_size, random_state=fold*random_seed)
		
		#! train model and make predictions
		model.fit(train_cv, y_target)
		preds = model.predict(test_cv)
		
		#! measure the error (difference between the predictions and the actual targets)
		mse = error.mse(y_true, preds)
		rmse = error.rmse(y_true, preds)
		rmsle = error.rmsle(y_true, preds)
		
		print "(fold %d of %d) MSE : %f | RMSE: %f | RMSLE: %f %s" % (fold + 1, folds, mse, rmse, rmsle, '')
		mses.append(mse); rmses.append(rmse); rmsles.append(rmsle)
		
	print ">>> Mean MSE: %f | Mean RMSE: %f | Mean RMSLE: %f <<<" % (np.mean(mses), np.mean(rmses), np.mean(rmsles))
	print "______________________________________________________________"
	
	if plot:
		plot_error(range(folds), rmsles,"Fold", "RMSLE", "Cross Validation using %s model" % model_name, ["RMSLE"])

        



# ---------------------- Scrap Notes ---------------------------------	
# models = [(linear_model.SGDRegressor, ), (linear_model.Ridge, ), ()]
# param_grid = {'alpha': [0.001, 0.01, 0.5]} #,1,5, 10, 100, 1000] }
#clf = linear_model.Ridge(alpha=a)
#clf = linear_model.SGDRegressor(alpha=0.2,n_iter=1000,shuffle=True)
#clf = linear_model.LassoCV(cv=3)
#clf = linear_model.ElasticNet()
#clf = linear_model.BayesianRidge()     
            
#clf = ensemble.RandomForestRegressor(n_estimators=100,random_state=42*idx*10,max_depth=4)
#clf = ensemble.ExtraTreesRegressor(n_estimators=100,random_state=42*idx*10,max_depth=4)
#clf = ensemble.GradientBoostingRegressor(alpha=a,n_estimators=100,random_state=42,max_depth=4)
                                                