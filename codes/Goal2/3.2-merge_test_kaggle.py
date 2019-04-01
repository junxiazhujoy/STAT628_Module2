import pandas as pd
import sklearn
from pandas import DataFrame


reviews_testsub = pd.read_csv("reviews_testsub_kaggle.csv") 

business_testsub = pd.read_csv("business_testsub_kaggle.csv") 

AllTestData = pd.merge(reviews_testsub,business_testsub,on='business_id',how='left')
print(AllTestData.head(10))

DataFrame.to_csv(AllTestData,"AllTestData_kaggle.csv",index=False)