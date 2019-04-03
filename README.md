# STAT628_Module2
Thu_group6

This repository contains analysis on Yelp data. We analyse yelp data focusing on nightlife and bars in Las Vegas. We aim to explore which factors influence ratings of reviews and furthermore give advice to owners for improving the ratings. Besides, we also construct prediction models for predicting ratings.

 + ***codes*** folder contains all python and r code we wrote.

    Note: For tidiness of this folder we exclude all csv and png files. If you want to execute our code, please copy all the   files in *data* and *image* folder making them under same path to avoid error. Sorry for the inconvenience.
     
     + **Goal1**
         + *attribute_analysis* 
             
             -- contains all codes doing attributes analysis such as tree methods and ANOVA
         + *review_analysis*
             1. data_cleaning/ -- contains all codes doing review data pre-processing
             2. extract_adj/ -- contains all codes doing adjective extraction near specific item
             3. ngrams_freq/ -- contains all codes doing single word/ngrams frequency and word cloud analysis
             4. shiny/ -- contains codes for shiny app
     + **Goal2**
         
         1. 1.* .py -- business data cleaning and extraction
         2. 2.* .py -- review data cleaning and extraction
         3. 3.* .py -- merge review and attritubes based on business_id
         4. 4.* .py -- model training
         5. 5-finalpre_kaggle.py -- produce final csv used on kaggle

+ ***data*** folder contains all files we used and created when performing analysis.
+ ***image*** folder contains all images we produced.
+ ***Report*** folder contains Jupyter Notebook summery of our results.

Team members:
+ Yingjing Jiang  (yjiang258@wisc.edu)
+ Yiqun Jiang  (yjiang257@wisc.edu)  
+ Junxia Zhu  (jzhu334@wisc.edu)
