import pandas as pd
import sklearn
from pandas import DataFrame


reviews_trainsub = pd.read_csv("reviews_trainsub_kaggle.csv") 

business_trainsub = pd.read_csv("business_trainsub_kaggle.csv") 

AllTrainData = pd.merge(reviews_trainsub,business_trainsub,on='business_id',how='left')
print(AllTrainData.head(10))

DataFrame.to_csv(AllTrainData,"AllTrainData_kaggle.csv",index=False)