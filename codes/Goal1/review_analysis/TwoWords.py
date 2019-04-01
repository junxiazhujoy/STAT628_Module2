import pandas as pd
import numpy as np
import json 
import copy
import csv
import os
import re
import nltk
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
from nltk.corpus import stopwords
import sklearn

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


dat_night_5star=[]
dat_night_4star=[]
dat_night_3star=[]
dat_night_2star=[]
dat_night_1star=[]
for i in range(len(dat_night)):
    if dat_night[i]['stars']=='5':
        dat_night_5star.append(dat_night[i])
    elif dat_night[i]['stars']=='4':
        dat_night_4star.append(dat_night[i])
    elif dat_night[i]['stars']=='3':
        dat_night_3star.append(dat_night[i])
    elif dat_night[i]['stars']=='2':
        dat_night_2star.append(dat_night[i])
    else:
        dat_night_1star.append(dat_night[i])



reviewslist = copy.deepcopy(dat_night_1star)
REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\$)|(\*)|(\%)|(\_)|(\=)|(\#)|(\&)|(\~)|(\@)")#[^\P{P}-]+
REPLACE_WITH_SPACE = re.compile("(\n)|(\-)|(\/)|(\d)")

def preprocess_reviews(reviews):
    reviews = REPLACE_NO_SPACE.sub("", reviews)
    reviews = REPLACE_WITH_SPACE.sub(" ", reviews)
    return reviews

reviewsTEXT_clean = copy.deepcopy(reviewslist)

text_cloud1=''

for ind in range(len(reviewslist)):
    texts = ''
    texts = reviewslist[ind]['text']
    texts = texts.lower()
    
    texts = re.sub('n\'t',' not', texts)
    
    texts = re.sub('isnt','isn\'t', texts)
    texts = re.sub('wasnt','wasn\'t', texts)
    texts = re.sub('werent','weren\'t', texts)
    texts = re.sub('dont','don\'t', texts)
    texts = re.sub('doesnt','doesn\'t', texts)
    texts = re.sub('didnt','didn\'t', texts)
    texts = re.sub('hasnt','hasn\'t', texts)
    texts = re.sub('havent','haven\'t', texts)
    texts = re.sub('hadnt','hadn\'t', texts)
    texts = re.sub('mightnt','mightn\'t', texts)
    texts = re.sub('shouldnt','shouldn\'t', texts)
    texts = re.sub('isn','isn\'t', texts)
    texts = re.sub('wasn','wasn\'t', texts)
    texts = re.sub('weren','weren\'t', texts)
    texts = re.sub('don','don\'t', texts)
    texts = re.sub('doesn','doesn\'t', texts)
    texts = re.sub('didn','didn\'t', texts)
    texts = re.sub('hasn','hasn\'t', texts)
    texts = re.sub('haven','haven\'t', texts)
    texts = re.sub('hadn','hadn\'t', texts)
    texts = re.sub('mightn','mightn\'t', texts)
    texts = re.sub('shouldn','shouldn\'t', texts)
    texts = re.sub('won\'t','will not', texts)
    texts = re.sub('n\'t',' not', texts)
    
    #add NOT_
    pattern = r'\.|\;|\!|\?|\,|\)|\(|\:|\'|\"|\%'
    list_text=re.split(pattern,texts)
    
    sent=''
    for i in range(len(list_text)):
        list_text[i] = re.sub('\+','', list_text[i])
        list_text[i] = re.sub('\*','', list_text[i])
        list_text[i] = re.sub('\$','', list_text[i])
        list_text[i] = re.sub('\[','', list_text[i])
        list_text[i] = re.sub('\]','', list_text[i])
        list_text[i] = re.sub('\%','', list_text[i])
        list_text[i] = re.sub('\\\\',' ', list_text[i])
        matchObj1 = re.search(r'(.*)not (.*)',list_text[i])
        matchObj2 = re.search(r'(.*) never (.*)',list_text[i])
        
        if matchObj1 != None :
            sub=re.sub(r' ', " notadd", matchObj1.group(2))
            list_text[i] = re.sub(matchObj1.group(2) ,sub, list_text[i])
            list_text[i] = re.sub(r'not ','', list_text[i],1)
            #list_text[i] = re.sub(',',' ', matchObj1.group(3))
            sent = sent + list_text[i] + ' '
        
        elif matchObj2 != None :
            sub=re.sub(r' ', " notadd", matchObj2.group(2))
            list_text[i] = re.sub(matchObj2.group(2) ,sub, list_text[i])
            list_text[i] = re.sub(r'never ','', list_text[i],1)
            #list_text[i] = re.sub(',',' ', matchObj1.group(3))
            sent = sent + list_text[i] + ' '
        
        else:
            sent = sent + list_text[i] + ' '


 text_clean=preprocess_reviews(sent)
 #print(text_clean)
    
 text_cloud1=text_cloud1+text_clean
 reviewsTEXT_clean[ind]['text']=text_clean
 reviewsTEXT_clean[ind]['text_split']=text_clean.split()
 ps = PorterStemmer()
 stem=[]
 for w in reviewsTEXT_clean[ind]['text_split']:
     stem.append(ps.stem(w))
 reviewsTEXT_clean[ind]['text_stem']=stem
 reviewsTEXT_clean[ind]['freq']=nltk.FreqDist(reviewsTEXT_clean[ind]['text_stem'])


stop_words = set(stopwords.words('english')) 
ps = PorterStemmer()
stop_words_stem=[]
for w in stop_words:
    stop_words_stem.append(ps.stem(w))
negWords=set(["wouldn't",'isn','wasn',"weren't", "haven't", "hasn't", "couldn't", "isn't", 'doesn','hasn',"mustn't", 'mightn', 'shan', 'no', "wasn't",'aren', "didn't", "hadn't","don't",'nor',"won't",'weren',"doesn't","needn't", 'shouldn',"mightn't","shan't", 'wouldn',"shouldn't",'hadn'])
negWords_stem=[]
for w in negWords:
    negWords_stem.append(ps.stem(w))
d=set(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','à','{sigh}'])
stopWords_stem=set(stop_words_stem)-set(negWords_stem)
stopWords_stem.update(d)

WORDS=[x for x in WORDS if x not in stopWords_stem]



def generate_ngrams(review, n):
    """
    Generate n-grams from a review
    :param review: one single review
    :param n: the size of n gram
    :return: generated list of n-grams
    """
    sentences = review.split(".")
    n_grams = []
    for sentence in sentences:
        sections = sentence.split(",")
        for section in sections:
            parts = section.split(";")
            for part in parts:
                words = part.split()
                
                n_grams_temp = []    # the return list
                for i in range(len(words)):
                    temp = words[i]
                    for j in range(1, n):
                        if (i + j) < len(words):
                            temp = temp + ' ' + words[i + j]
                            n_grams.append(temp)
    return n_grams


from stemming.porter2 import stem
allReviews=[x['text'] for x in reviewsTEXT_clean]
rvs2= [" ".join([stem(word) for word in sentence.split(" ")]) for sentence in allReviews]
twoWords = {}
for i in rvs2:
    twoWdLs=generate_ngrams(i, 2)
    for j in twoWdLs:
        if j in twoWords:
            twoWords[j]=twoWords[j]+1
        else:
            twoWords[j]=1
#twoWords



ToRemove=set()
for i in stopWords_stem:
    for j in stopWords_stem:
        temp=i + ' ' + j
        ToRemove.add(temp)
#ToRemove
for i in ToRemove:
    if i in twoWords:
        twoWords.pop(i)
#twoWords

sorted(twoWords.items(), key=lambda x: x[1],reverse=True)

































