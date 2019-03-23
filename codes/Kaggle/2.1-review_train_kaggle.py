import json
import pandas as pd
import numpy as np
import re
import copy
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.stem import PorterStemmer


data = [] 
for line in open('review_train.json', 'r'): 
    data.append(json.loads(line))


######!!!!!!!!!!!######
dat = data[0:1000000]


reviewslist = copy.deepcopy(dat)




REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\$)|(\*)|(\%)|(\_)|(\=)|(\#)|(\&)|(\~)|(\@)")#[^\P{P}-]+
REPLACE_WITH_SPACE = re.compile("(\n)|(\-)|(\/)|(\d)")

def preprocess_reviews(reviews):
    reviews = REPLACE_NO_SPACE.sub("", reviews)
    reviews = REPLACE_WITH_SPACE.sub(" ", reviews)
    
    return reviews

reviewsTEXT_clean = copy.deepcopy(reviewslist)

for ind in range(len(reviewslist)):
    texts = ''
    texts = reviewslist[ind]['text']
    texts = texts.lower()
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
   
    #print(sent)
    #print(texts)
    #print(texts)
    text_clean=preprocess_reviews(sent)
    #print(text_clean)
    reviewsTEXT_clean[ind]['text']=text_clean
    reviewsTEXT_clean[ind]['text_split']=text_clean.split()
    ps = PorterStemmer()
    stem=[]
    for w in reviewsTEXT_clean[ind]['text_split']:
        stem.append(ps.stem(w))
    reviewsTEXT_clean[ind]['text_stem']=stem
    reviewsTEXT_clean[ind]['freq']=nltk.FreqDist(reviewsTEXT_clean[ind]['text_stem'])
    
#reviewsTEXT_clean[0]


with open("review_train_pre.json", 'w') as fp:
        json.dump(reviewsTEXT_clean, fp)


#reviewsTEXT_clean=[]
#for line in open('review_train_pre.json', 'r'): 
#    reviewsTEXT_clean.append(json.loads(line))




#select words due to frequency order
AllFreq = reviewsTEXT_clean[0]['freq']
for ind in range(len(reviewsTEXT_clean)-1):
    freqs = reviewsTEXT_clean[ind+1]['freq']
    AllFreq.update(freqs)
    
wordList = sorted(AllFreq.items(),key=lambda item:item[1],reverse=True)

#choose the important ones--No.1-100
WORDS=[x[0] for x in wordList]
WORDS=WORDS[0:2000]




#stop_words = set(stopwords.words('english')) 
stop_words = {'who', 'how', 'him', 'can', 'than', 'these', 'your', 'the', 'while', 'don', 'of', 'on', 'had', 'there', "you've", 'that', 'having', 'himself', "mustn't", 'same', 'are', "won't", 'then', 'itself', 'doing', 'from', 'both', 'where', 'wouldn', 'me', 'off', 'because', 'isn', "you'd", 'whom', 'mustn', 'is', 'themselves', 'no', 'very', 'up', 'd', 'ma', 'yours', 'been', 'ain', 'will', 'a', 'most', 'did', 'with', 'o', 'this', 'during', 'i', "mightn't", "isn't", 'being', 'couldn', 'them', 'not', 'such', 'her', 'some', 'only', "didn't", 'should', 'after', 'our', 'down', 'here', 'about', 'herself', "hadn't", 'but', 'he', 'an', 'am', 't', 'they', 'again', 'll', 've', 'didn', 'into', 'needn', 're', 'nor', "couldn't", 'above', 'all', "should've", 'm', 'other', 'below', "she's", 'just', 'between', 'hasn', 'own', 'yourselves', 'until', 'too', 'which', "shouldn't", 's', "it's", 'his', 'y', 'to', 'over', 'hadn', "shan't", 'does', 'weren', 'shouldn', 'under', "aren't", 'be', "don't", 'any', 'or', "haven't", 'she', 'aren', 'against', 'we', 'in', 'ourselves', 'have', 'won', "wasn't", 'wasn', 'you', 'what', 'mightn', "weren't", 'doesn', 'hers', 'myself', 'shan', 'before', 'more', "wouldn't", 'were', 'each', "doesn't", 'through', 'for', "hasn't", 'by', 'now', 'do', 'has', 'those', 'few', "you'll", 'once', 'it', 'their', 'further', "you're", 'my', 'at', 'when', 'yourself', 'why', 'as', 'was', 'and', 'out', "needn't", 'if', 'haven', 'its', 'theirs', "that'll", 'so', 'ours'}
ps = PorterStemmer()
stop_words_stem=[]
for w in stop_words:
    stop_words_stem.append(ps.stem(w))
negWords=set(["wouldn't",'isn','wasn',"weren't", "haven't", "hasn't", "couldn't", "isn't", 'doesn','hasn',"mustn't", 'mightn', 'shan', 'no', "wasn't",'aren', "didn't", "hadn't","don't",'nor',"won't",'weren',"doesn't","needn't", 'shouldn',"mightn't","shan't", 'wouldn',"shouldn't",'hadn'])
stop_words_negWords=[]
for w in negWords:
    stop_words_negWords.append(ps.stem(w))
d=set(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','à'])
stopWords=set(stop_words_stem)-set(stop_words_negWords)
stopWords.update(d)

WORDS=[x for x in WORDS if x not in stopWords]



print('high-frequency words:')
print(WORDS)





for i in range(len(reviewsTEXT_clean)):
    reviewsTEXT_clean[i]['text'] = ''
    for ind in reviewsTEXT_clean[i]['text_split']:
        if ind in WORDS:
            reviewsTEXT_clean[i]['text'] = reviewsTEXT_clean[i]['text'] + ind +' '
        else:
            reviewsTEXT_clean[i]['text'] = reviewsTEXT_clean[i]['text']





#create list of texts
texts= [x['text'] for x in reviewsTEXT_clean]





#vectorizer = CountVectorizer(token_pattern=r'\b[^\d\W]+\b')
vectorizer = CountVectorizer()
#X = vectorizer.fit_transform(texts)
transformer = TfidfTransformer()

tfidf = transformer.fit_transform(vectorizer.fit_transform(texts))

X=tfidf





#vectorizer.get_feature_names()
X_df=pd.DataFrame(X.A,columns=vectorizer.get_feature_names())




Reviews_df=X_df[WORDS]
print(Reviews_df.head(10))




#Add Business ID in the data frame
businessIDs=[x['business_id'] for x in reviewsTEXT_clean]
Reviews_df['business_id']=businessIDs
print(Reviews_df.head(10))





#Add stars in the data frame
stars=[x['stars'] for x in reviewsTEXT_clean]
Reviews_df['Stars']=stars
print(Reviews_df.head(10))




from pandas import DataFrame
DataFrame.to_csv(Reviews_df,"review_train_kaggle.csv",index=False)


#col=Reviews_df.columns.values

#DataFrame.to_csv(pd.DataFrame(col),"review_train_kaggle_colnames.csv",index=False)











