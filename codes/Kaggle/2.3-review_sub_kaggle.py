import pandas as pd
import sklearn
from pandas import DataFrame



reviews_train=pd.read_csv("review_train_kaggle.csv")
reviews_train_dummy=pd.get_dummies(reviews_train)

reviews_test=pd.read_csv("review_test_kaggle.csv")
reviews_test_dummy=pd.get_dummies(reviews_test)

reviews_index = list(set(reviews_train_dummy.columns) & set(reviews_test_dummy.columns))






reviews_trainsub=reviews_train_dummy[reviews_index]

DataFrame.to_csv(reviews_trainsub,"reviews_trainsub_kaggle.csv",index=False)

DataFrame.to_csv(pd.DataFrame(reviews_train['Stars']),"stars_kaggle.csv",index=False)



reviews_testsub=reviews_test_dummy[reviews_index]

DataFrame.to_csv(reviews_testsub,"reviews_testsub_kaggle.csv",index=False)