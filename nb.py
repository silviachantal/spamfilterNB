# I import the corpus module, defaultdict for counting words and math module for log operations
from collections import defaultdict
from corpus import *
from typing import *
import math


class SpamFilter:
    def __init__(self):
        # I create a defaultdict with default value one for the Laplace smoothing. More info under the classify() function
        self.spam_word_count = defaultdict(lambda: 1)
        self.ham_word_count = defaultdict(lambda: 1)

        # Spam and ham mails are equally probable so I set a default value of 0.5 for both that will be incremented
        self.spam_prob = 0.5
        self.ham_prob = 0.5

    def train(self, emails: List[Tuple[List[str], str]]):
        spam_mails = []
        ham_mails = []

        # I iterate over each email and append its content in the corresponding spam or ham list
        for (words, label) in emails:
            if label == "spam":
                spam_mails.append(words)
            elif label == "ham":
                ham_mails.append(words)

        # I iterate over the tokens of each email and increase the corresponding deafultdict key by one as a specific word is encountered either in spam or ham
        for words in spam_mails:
            for word in words:
                self.spam_word_count[word] += 1
        for words in ham_mails:
            for word in words:
                self.ham_word_count[word] += 1

        # I update the probability counter
        self.ham_prob = len(ham_mails) / len(emails)
        self.spam_prob = len(spam_mails) / len(emails)

    def classify(self, email):
        # I set a variable with default value zero to which I will add the total score of each email to evaluate
        spam_email_score = 0
        ham_email_score = 0
        # I sum the values of the spammy and hammy words from the training
        total_spam_count = sum(self.spam_word_count.values())
        total_ham_count = sum(self.ham_word_count.values())

        # I want to get the spam and ham score of each word in the mail I want to classify & add it to the overall mail score
        # I ask myself "in how many spam and/or ham emails does this word appear?"
        # Then I increment the overall email score for each word's score
        # To increment I use log function to solve the problem of finding new words during the classification, not found during training
        # Log(0) is undefined and woult throw an error: I set 1 as default value in defaultdict as mentioned above(Laplace Smooting)
        for word in email:
            word_spam_score = self.spam_word_count[word] / (total_spam_count)
            # Here I compute the overall probability by summing all single words' probabilities
            spam_email_score += math.log(word_spam_score)
            word_ham_score = self.ham_word_count[word] / (total_ham_count)
            ham_email_score += math.log(word_ham_score)

        spam_email_score += math.log(self.spam_prob)
        ham_email_score += math.log(self.ham_prob)

        # I compare the two scores and use formatting for returning only three decimals
        if spam_email_score > ham_email_score:
            return ("{:.3f}".format(spam_email_score)), "spam"
        else:
            return ("{:.3f}".format(ham_email_score)), "ham"
