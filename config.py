"""
model definitions 
"""

model_config = (
		{'from':['sklearn'],
		'module':'sklearn.linear_model',
		'name':'Ridge',
		'kwargs': {'alpha':0.25},
		'seed_range':range(1),
		'feature_imp':False
		},
		{'from':['sklearn'],
		'module':'sklearn.linear_model',
		'name':'SGDRegressor',
		'kwargs': {'alpha':0.25, 'shuffle':True, 'n_iter':100},
		'seed_range':range(1),
		'feature_imp':False
		},
		{'from':['sklearn'],
		'module':'sklearn.linear_model',
		'name':'LassoCV',
		'kwargs': {'alphas':[0.001, 0.1, 0.25, 0.5, 1, 10, 100, 1000], 'max_iter':100},
		'seed_range':range(1),
		'feature_imp':False
		},
		{'from':['sklearn'],
		'module':'sklearn.linear_model',
		'name':'ElasticNet',
		'kwargs': {'alpha':0.25, 'max_iter':100},
		'seed_range':range(1),
		'feature_imp':False
		},
		{'from':['sklearn'],
		'module':'sklearn.linear_model',
		'name':'BayesianRidge',
		'kwargs': {'alpha_1':0.0000001, 'alpha_2':0.0000001, 'n_iter':300},
		'seed_range':range(1),
		'feature_imp':False
		},
		{'from':['sklearn'],
		'module':'sklearn.ensemble',
		'name':'RandomForestRegressor',
		'kwargs': {'n_estimators':500, 'random_state':42, 'max_depth':5},
		'seed_range':range(5),
		'feature_imp':True
		},
		{'from':['sklearn'],
		'module':'sklearn.ensemble',
		'name':'ExtraTreesRegressor',
		'kwargs': {'n_estimators':500, 'random_state':42, 'max_depth':5},
		'seed_range':range(1),
		'feature_imp':True
		},
		{'from':['sklearn'],
		'module':'sklearn.ensemble',
		'name':'GradientBoostingRegressor',
		'kwargs': {'alpha':0.25, 'n_estimators':200, 'random_state':42, 'max_depth':3},
		'seed_range':range(1),
		'feature_imp':True
		})

