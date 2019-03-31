import pandas as pd
import numpy as np
import json 
import copy
import csv
import os
import re
import nltk
import sklearn
import nltk
from nltk.corpus import stopwords
import sklearn
from nltk.stem import PorterStemmer

data = [] 
cf = open('bars_rev_tr_df.csv','r')

file = csv.DictReader(cf)
#print(file.fieldnames)

for x in file:
    line = {'business_id':x['business_id'],'date':x['date'],'stars':x['stars'],'text':x['text']}
    data.append(line)

cf.close()

id = open('uniq_id_lvbars.txt','r')
id_str=id.read()
id.close()

id_list=id_str.split(',')

dat_night=[]
for i in range(len(data)):
    if data[i]['business_id'] in id_list:
        dat_night.append(data[i])




reviewslist = copy.deepcopy(dat_night)
reviewsTEXT_clean = copy.deepcopy(reviewslist)


adj_list=[]
for i in range(len(dat_night)):
    text=nltk.word_tokenize(dat_night[i]['text'])
    token=nltk.pos_tag(text)
    adj=[]
    for m in range(len(token)):
        if token[m][1]=='JJ':
            adj.append(token[m][0])
    if 'cocktail' in dat_night[i]['text']:
        temp_list=dat_night[i]['text'].split()
        for i in range(len(temp_list)-2):
            if ((temp_list[i]=='cocktail') and (temp_list[i+1]=='is' or temp_list[i+1]=='was')) and (temp_list[i+2] in adj):
                adj_list.append(temp_list[i+2].lower())
            elif (temp_list[i]=='cocktail'):
                if (temp_list[i-2] in adj):
                    adj_list.append(temp_list[i-2].lower())
                elif (temp_list[i-1] in adj):
                    adj_list.append(temp_list[i-1].lower()) 
                elif (temp_list[i+1] in adj):
                    adj_list.append(temp_list[i+1].lower()) 
                elif (temp_list[i+2] in adj):
                    adj_list.append(temp_list[i+2].lower()) 

stop_words = set(stopwords.words('english')) 
negWords=set(["wouldn't",'isn','wasn',"weren't", "haven't", "hasn't", "couldn't", "isn't", 'doesn','hasn',"mustn't", 'mightn', 'shan', 'no', "wasn't",'aren', "didn't", "hadn't","don't",'nor',"won't",'weren',"doesn't","needn't", 'shouldn',"mightn't","shan't", 'wouldn',"shouldn't",'hadn'])
d=set(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','à','{sigh}'])
stopWords=stop_words-negWords
stopWords.update(d)
adj_list=[x for x in adj_list if x not in stopWords]

adj_set_cocktail = set(adj_list)

file=open('cocktail_adj.txt','w') 
file.write(str(adj_set_cocktail)); 
file.close()
