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

from sklearn.linear_model import SGDClassifier

#Initializing Classifiers                                                                                                                       
clf5 = SGDClassifier(average=True,alpha=0.0001,random_state=1,class_weight='balanced', loss='log',n_jobs=1,shuffle=True)


#Setting up the parameter grids                                                                                                                 
param_grid5 = [{'max_iter': list(range(4, 6, 1))}]



# Setting up multiple GridSearchCV objects, 1 for each algorithm                                                                                
gcv = GridSearchCV(estimator=clf5,
                   param_grid=param_grid5,
                   scoring='neg_mean_squared_error',
                   cv=10)

gcv.fit(AllTrainData.drop(columns='business_id'),stars)

print('SGDClassifier:')
print('MSE %.2f (average over 10-fold CV folds)' % (gcv.best_score_))
print('Best Parameters: %s' % gcv.best_params_)



#Prediction                                                                                                                                     
final_model=gcv.best_estimator_
predict_y=final_model.predict(AllTestData.drop(columns='business_id'))
#metrics.f1_score(y, predict_y)                                                                                                                 
print(pd.DataFrame(predict_y).head(10))



#####                                                                                                                                           
#X_test_fs = gs.best_estimator_.named_steps['fs'].transform(X_test)                                                                             
#pred = gs.best_estimator_.named_steps['clf'].predict(X_test_fs)                                                                                

DataFrame.to_csv(pd.DataFrame(predict_y),"pred_asgdclass_balanced_log.csv",index=False)