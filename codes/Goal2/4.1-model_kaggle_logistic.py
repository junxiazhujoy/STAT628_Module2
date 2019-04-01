import pandas as pd
import sklearn
from pandas import DataFrame


AllTrainData = pd.read_csv("AllTrainData_kaggle.csv")
print(AllTrainData.head(10))

AllTestData = pd.read_csv("AllTestData_kaggle.csv") 
print(AllTestData.head(10))

stars=pd.read_csv("stars_kaggle.csv")
print(stars.head(10))

import numpy as np
stars=np.array(stars['Stars'])
print(stars)





import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier



#Initializing Classifiers
clf1 = LogisticRegression(multi_class='multinomial',
                          solver='newton-cg',
                          random_state=1)

#Building the pipelines
pipe1 = Pipeline([('std', StandardScaler()),
                  ('clf1', clf1)])


#Setting up the parameter grids
param_grid1 = [{'clf1__penalty': ['l2'],
                'clf1__C': np.power(10., np.arange(-4, 4))}]





# Setting up multiple GridSearchCV objects, 1 for each algorithm
gcv = GridSearchCV(estimator=pipe1,
                   param_grid=param_grid1,
                   scoring='neg_mean_squared_error',
                   cv=5)

gcv.fit(AllTrainData.drop(columns='business_id'),stars)

print('LogisticRegression:')
print('MSE %.2f (average over 5-fold CV folds)' % (gcv.best_score_))
print('Best Parameters: %s' % gcv.best_params_)





#Prediction
final_model=gcv.best_estimator_
predict_y=final_model.predict(AllTestData.drop(columns='business_id'))
#metrics.f1_score(y, predict_y)
print(pd.DataFrame(predict_y).head(10))



#####
#X_test_fs = gs.best_estimator_.named_steps['fs'].transform(X_test)
#pred = gs.best_estimator_.named_steps['clf'].predict(X_test_fs)




DataFrame.to_csv(pd.DataFrame(predict_y),"pred_logistic.csv",index=False)





