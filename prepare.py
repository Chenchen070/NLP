import unicodedata
from bs4 import BeautifulSoup
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
import pandas as pd
from requests import get

import acquire

def basic_clean(text):
    article = text.lower()
    article = unicodedata.normalize('NFKD', article)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    article = re.sub(r"[^a-z0-9'\s]", '', article)
    return article 

def tokenize(text):
    tokenizer = nltk.tokenize.ToktokTokenizer()
    article = tokenizer.tokenize(text, return_str=True)
    return article

def stem(text):
    ps = nltk.stem.porter.PorterStemmer()
    stems = [ps.stem(word) for word in text.split()]
    article_stemmed = ' '.join(stems)
    return article_stemmed  

def lemmatize(text):    
    wnl = nltk.stem.WordNetLemmatizer()    
    lemmas = [wnl.lemmatize(word) for word in text.split()]    
    lemmatized_string = ' '.join(lemmas)    
    return lemmatized_string

def remove_stopwords(string, extra_words=None, exclude_words=None):    
    stopword_list = stopwords.words('english')    
    if exclude_words:        
        stopword_list = stopword_list + exclude_words
        
    if extra_words:        
        for word in extra_words:            
            stopword_list.remove(word)
            
    words = string.split()    
    filtered_words = [word for word in words if word not in stopword_list]    
    filtered_string = ' '.join(filtered_words)   
    return filtered_string

