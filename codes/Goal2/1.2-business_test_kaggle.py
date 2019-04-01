import json
import pandas as pd
import numpy as np
import re
from pandas import DataFrame
import copy


data = [] 
for line in open('business_test.json', 'r'): 
    data.append(json.loads(line))


dat = data

#pd.DataFrame.from_dict(dat)




def fun(KeyString,Diction,newlist):
    if '{' not in str(Diction[KeyString]):
            newlist[KeyString]=str(Diction[KeyString])
    else:
        d=eval(str(Diction[KeyString]))
        for k in d.keys():
            fun(k,d,newlist)


for i in range(len(dat)):#len(dat)  
    attri=dat[i]['attributes']
    if attri!=None:
        newlist={}
        for k in attri.keys():
            fun(k,attri,newlist) 
    dat[i]['attributes_clean']=newlist

#TODO: cat the names together




AllAttributes=[x['attributes_clean'] for x in dat] #a list of dictionaries
#transform into one dictionary
attridf=pd.DataFrame.from_dict(AllAttributes)
#attridf




for i in range(len(attridf['Alcohol'])):
    if str(attridf['Alcohol'][i]).startswith('u\''):
        strinfo=re.compile('u\'')
        attridf['Alcohol'][i]=str(eval(strinfo.sub('\'',str(attridf['Alcohol'][i]))))
    elif str(attridf['Alcohol'][i]).startswith('\''):
            attridf['Alcohol'][i] = str(eval(attridf['Alcohol'][i]))

for i in range(len(attridf['RestaurantsAttire'])):
    if str(attridf['RestaurantsAttire'][i]).startswith('u\''):
        strinfo=re.compile('u\'')
        attridf['RestaurantsAttire'][i]=str(eval(strinfo.sub('\'',str(attridf['RestaurantsAttire'][i]))))
    elif str(attridf['RestaurantsAttire'][i]).startswith('\''):
            attridf['RestaurantsAttire'][i] = str(eval(attridf['RestaurantsAttire'][i]))
        
for i in range(len(attridf['NoiseLevel'])):
    if str(attridf['NoiseLevel'][i]).startswith('u\''):
        strinfo=re.compile('u\'')
        attridf['NoiseLevel'][i]=str(eval(strinfo.sub('\'',str(attridf['NoiseLevel'][i]))))
    elif str(attridf['NoiseLevel'][i]).startswith('\''):
        attridf['NoiseLevel'][i] = str(eval(attridf['NoiseLevel'][i]))
        
for i in range(len(attridf['WiFi'])):
    if str(attridf['WiFi'][i]).startswith('u\''):
        strinfo=re.compile('u\'')
        attridf['WiFi'][i]=str(eval(strinfo.sub('\'',str(attridf['WiFi'][i]))))
    elif str(attridf['WiFi'][i]).startswith('\''):
        attridf['WiFi'][i] = str(eval(attridf['WiFi'][i]))
        
for i in range(len(attridf['BYOBCorkage'])):
    if str(attridf['BYOBCorkage'][i]).startswith('u\''):
        strinfo=re.compile('u\'')
        attridf['BYOBCorkage'][i]=str(eval(strinfo.sub('\'',str(attridf['BYOBCorkage'][i]))))
    elif str(attridf['BYOBCorkage'][i]).startswith('\''):
        attridf['BYOBCorkage'][i] = str(eval(attridf['BYOBCorkage'][i]))
        
for i in range(len(attridf['Smoking'])):
    if str(attridf['Smoking'][i]).startswith('u\''):
        strinfo=re.compile('u\'')
        attridf['Smoking'][i]=str(eval(strinfo.sub('\'',str(attridf['Smoking'][i]))))
    elif str(attridf['Smoking'][i]).startswith('\''):
        attridf['Smoking'][i] = str(eval(attridf['Smoking'][i]))        
        
for i in range(len(attridf['AgesAllowed'])):
    if str(attridf['AgesAllowed'][i]).startswith('u\''):
        strinfo=re.compile('u\'')
        attridf['AgesAllowed'][i]=str(eval(strinfo.sub('\'',str(attridf['AgesAllowed'][i]))))
    elif str(attridf['AgesAllowed'][i]).startswith('\''):
        attridf['AgesAllowed'][i] = str(eval(attridf['AgesAllowed'][i]))
        
for i in range(len(attridf['AgesAllowed'])):
    if str(attridf['AgesAllowed'][i]).startswith('u\''):
        strinfo=re.compile('u\'')
        attridf['AgesAllowed'][i]=str(eval(strinfo.sub('\'',str(attridf['AgesAllowed'][i]))))
    elif str(attridf['AgesAllowed'][i]).startswith('\''):
        attridf['AgesAllowed'][i] = str(eval(attridf['AgesAllowed'][i]))





#TODO:NaN change to None.
#ColumnNames=attridf.columns
'''
for i in ColumnNames:
    x for x in attridf[[i]]
'''
isNaN=pd.isnull(attridf)
attridf[pd.isnull(attridf)]='unknown'
#attridf




#Add Business ID in the data frame
businessIDs=[x['business_id'] for x in dat]
attridf['business_id']=businessIDs
#attridf




attridf2 = copy.deepcopy(attridf)




col=[x.upper() for x in attridf2.columns.values]
col[len(col)-1]=col[len(col)-1].lower()




attridf2.columns=list(col)
print(attridf2.head(10))



DataFrame.to_csv(attridf2,"business_test_kaggle.csv",index=False)
#DataFrame.to_csv(pd.DataFrame(col),"business_train_kaggle_2_colnames.csv",index=False)


