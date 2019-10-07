#### Logistic Regression
lr_dict = {'classifier': {'model': 'lr', 'fixed_args': {'random_state': 27}},
            'classifier__penalty': ['l1', 'l2'],
            'classifier__C': [i for i in range(60)]}

#### Linear Discriminant Analysis
lda_dict = {'classifier': {'model': 'lda', 'fixed_args': {}}}

#### Naive Bayes
nb_dict = {'classifier': {'model': 'nb', 'fixed_args': {}}}

#### SVM
C = [0.1, 0.5, 1, 5, 10, 20, 50, 100]
kernel = ['linear', 'poly', 'rbf', 'sigmoid']
svm_dict = {'classifier': {'model': 'svm', 'fixed_args': {'gamma': 'scale', 'probability': True}},
            'classifier__C': C,
            'classifier__kernel': kernel}

#### kNN
knn_dict = {'classifier': {'model': 'knn', 'fixed_args': {'n_jobs': -1}},
            'classifier__n_neighbors': [i for i in range(1, 60)]}

#### CART
cart_dict = {'classifier': {'model': 'cart', 'fixed_args': {'random_state': 27}},
            'classifier__max_features': ['auto', 'log2', None]}

#### Random Forest
rf_dict = {'classifier': {'model': 'rf', 'fixed_args': {'n_jobs': -1, 'random_state': 27}},
            'classifier__n_estimators': [i for i in range(100, 300)],
            'classifier__max_features': ['auto', 'log2', None]}

#### Light GBM
lgb_dict = {'classifier': {'model': 'lgb_', 'fixed_args': {'n_jobs': -1, 'random_state': 27}},
            'classifier__n_estimators': [i for i in range(100, 300)]}

####  Xtreme Gradient Boosting
xgb_dict = {'classifier': {'model': 'xgb_', 'fixed_args': {'n_jobs': -1, 'random_state': 27}},
            'classifier__n_estimators': [i for i in range(100, 300)],
            'classifier__booster': ['dart', 'gblinear', 'gbtree']}

#### AdaBoost
adaboost_dict = {'classifier': {'model': 'adaboost', 'fixed_args': {}},
                 'classifier__n_estimators': [i for i in range(100, 300)]}

# All models
models = [lr_dict,
          lda_dict,
          nb_dict,
          knn_dict,
          cart_dict,
          rf_dict,
          lgb_dict,
          xgb_dict,
          adaboost_dict]