from collections import defaultdict
from matplotlib.pyplot import cla
from corpus import * #page 68 "this is considered bad practice"
from typing import *
import math

class SpamFilter:
    def __init__(self):
        self.spam_word_count = defaultdict(lambda:1)
        self.ham_word_count = defaultdict(lambda:1)

        self.spam_prob =  0.5
        self.ham_prob = 0.5

        
    def train(self, emails : List[Tuple[List[str], str]]): 
        spam_mails = []
        ham_mails = []

        for (words, label) in emails:
            if label == "spam":
                spam_mails.append(words)
            elif label == "ham":
                ham_mails.append(words)   
        
        for words in spam_mails:
            for word in words:
                self.spam_word_count[word] += 1
        for words in ham_mails:
            for word in words:
                self.ham_word_count[word] += 1
            
        self.ham_prob = len(ham_mails)/len(emails)
        self.spam_prob = len(spam_mails)/len(emails)
                       
       
    def classify (self, email):   
        spam_email_score = 0 
        ham_email_score = 0

        for word in email:
            word_spam_score = self.spam_word_count[word]/(sum(self.spam_word_count.values()))
            spam_email_score += math.log(word_spam_score)
            word_ham_score = self.ham_word_count[word]/(sum(self.ham_word_count.values()))    
            ham_email_score += math.log(word_ham_score)
        
        spam_email_score += math.log(self.spam_prob)
        ham_email_score += math.log(self.ham_prob)

        if spam_email_score > ham_email_score:
            return ("{:.3f}".format(spam_email_score)), "spam"
        else:
            return ("{:.3f}".format(ham_email_score)), "ham"
