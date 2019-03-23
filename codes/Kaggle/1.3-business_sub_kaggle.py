import pandas as pd
import sklearn
from pandas import DataFrame



business_train=pd.read_csv("business_train_kaggle.csv")
business_train_dummy=pd.get_dummies(business_train)

business_test=pd.read_csv("business_test_kaggle.csv")
business_test_dummy=pd.get_dummies(business_test)

business_index = list(set(business_train_dummy.columns) & set(business_test_dummy.columns))






business_trainsub=business_train_dummy[business_index]

DataFrame.to_csv(business_trainsub,"business_trainsub_kaggle.csv",index=False)



business_testsub=business_test_dummy[business_index]

DataFrame.to_csv(business_testsub,"business_testsub_kaggle.csv",index=False)