# I import the libraries I will need for tokenizing and cleaning our data
from collections import Counter
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

# I use nltk because it considers less words than other libraries
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))
stop_words_es = set(stopwords.words("spanish"))
stop_words_de = set(stopwords.words("german"))
# from nltk.tokenize import word_tokenize
import re
from typing import *

# instead of using the os library
from pathlib import Path

# for tokenizing I set ignoretiny to false because with true the recall performance was lower
def tokenize(text, ignoretiny=False):
    pattern = r"(?:[A-Z]\.)+|\w+(?:-\w+)*"
    onlyalphanum_tok = nltk.regexp_tokenize(text, pattern)[
        1:
    ]  # to always avoid "Subject:"

    lowercase_tok = [w.lower() for w in onlyalphanum_tok]
    useful_tok = [w for w in lowercase_tok if w not in stop_words]
    useful_tok = [w for w in useful_tok if w not in stop_words_es]
    useful_tok = [w for w in useful_tok if w not in stop_words_de]
    # optional tiny words
    if ignoretiny:
        useful_tok = [w for w in useful_tok if len(w) >= 3]
    vocab = sorted(set(useful_tok))
    return vocab


# this functions accesses the content of each email and divides it into tokens
def read_file(path):
    with open(path, "r", errors="ignore", encoding="latin-1") as file:
        content = (
            file.read()
        )  # the read method creates a string with the contents of the entire file
        email_tok = tokenize(content)
        return email_tok


# this function accesses the dataset of emails both in the spam and in the ham directory
def read_dataset(path):
    dataset_location = Path(path)
    assert dataset_location.is_dir()

    ham_dir = dataset_location.joinpath("ham")
    spam_dir = dataset_location.joinpath("spam")

    trainset = []
    # I retrieve the files inside the two directories by checking that their path ends with txt extension
    for hamfile in ham_dir.glob("*.txt"):
        # I read the content of each file and append it with its label for later training
        ham_comb = read_file(hamfile)
        trainset.append((ham_comb, "ham"))

    for spamfile in spam_dir.glob("*.txt"):
        spam_comb = read_file(spamfile)
        trainset.append((spam_comb, "spam"))

    return trainset
