import pandas as pd
from pandas import DataFrame
import numpy as np


pre=pd.read_csv("pred_rfclassifier.csv")
finalpre=DataFrame(np.arange(pre.shape[0])+1,columns=['ID'])
finalpre['Expected']=pre['0']
print(finalpre.head(10))

DataFrame.to_csv(finalpre,"finalpre_rfclassifier.csv",index=False)