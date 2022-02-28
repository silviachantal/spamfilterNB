# I import the libraries I will need for tokenizing and cleaning our data
#from sklearn.feature_extraction.text import CountVectorizer
from asyncore import read
from collections import Counter
import numpy as np
import nltk
#import matplotlib.pyplot as pb
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords #I use nltk because it has less than other libr, I don't want to lose 2 much info
stop_words = set(stopwords.words('english'))
stop_words_es = set(stopwords.words('spanish'))
stop_words_de = set(stopwords.words('german'))
#from nltk.tokenize import word_tokenize
#import os  #no, i use pathlib
import re  # but i will use nltk stemmer: we might use regex to get words without suffixes? nah
from typing import *
from pathlib import Path
# browsing the natural language toolkit's available packages. This consists of 30 compressed files, requiring about 100Mb disk space. Downloaded to my machine.



def tokenize(text):
    pattern = r'(?:[A-Z]\.)+|\w+(?:-\w+)*'
    onlyalphanum_tok = nltk.regexp_tokenize(text, pattern)[1:] #to always avoid "Subject"
    lowercase_tok = [w.lower() for w in onlyalphanum_tok]
    useful_tok_en = [w for w in lowercase_tok if w not in stop_words] #TODO:i try keeping all default stopwords
    useful_tok_es = [w for w in useful_tok_en if w not in stop_words_es]
    useful_tok_de = [w for w in useful_tok_es if w not in stop_words_de]
    useful_tok = [w for w in useful_tok_de if len(w) >= 3]
    vocab = sorted(set(useful_tok))
    return vocab
    #text cleaning: stopwords with nltk (+ adding and removign)? I just want to remove articles and pronouns? or scikitlearn?
    #i could train it once with punct and once without 
    #  # naive bayes is naive because it treats words unrelationally like a vocab
    
    
def read_file(path):
    with open(path, "r", errors = "ignore", encoding ="latin-1") as file:
        content=file.read()  # the read method creates a string with the contents of the entire file
        email_tok = tokenize(content)
        return email_tok
    

def read_dataset(path):
    dataset_location = Path(path)
    assert dataset_location.is_dir()
    
    ham_dir = dataset_location.joinpath('ham')
    spam_dir = dataset_location.joinpath('spam')
    
    trainset = []

    for hamfile in ham_dir.glob('*.txt'):
        ham_comb = read_file(hamfile)
        trainset.append((ham_comb, "ham"))

    for spamfile in spam_dir.glob('*.txt'):
        spam_comb = read_file(spamfile)
        trainset.append((spam_comb, "spam"))

    return trainset

myexamp = read_dataset("data/data/train")
print(myexamp)