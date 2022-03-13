#the hitchikers guide to pyhton 
#https://python-docs.readthedocs.io/en/latest/writing/structure.html
#chapter 4: strcturing your code(p65)

#this module "main.py" is the abstraction layer of the project that handles interfacing with user actions
#i will hence import my project's internal modules

#command-line application 
#i will use argparse library because it is in the Python's standard library

import argparse
import corpus 
import nb
from nb import SpamFilter

      
def create_parser():
    parser = argparse.ArgumentParser(description="filters email contents dividing them into two categories: ham or spam") #the parser will hold all the information necessary to parse the command-line into python datatypes
    parser.add_argument('-tr', '--train_dataset', metavar='dataset path', required='True', type=str, help='enter a path to a dataset of emails on which the filter will be trained') #we define which arguments the program will require: we tell how to take strings in CLI and turn them into objects
    parser.add_argument('-te', '--test_dataset', metavar='dataset path', required='True', type=str, help='enter a path to a dataset of emails on which the filter will be tested')
    parser.add_argument('-f', '--resultfile', metavar='file', required='True', type=str, help='enter a path to a file where you want the results to be stored')
    parser.add_argument('-ud', '--diremails_classify', metavar='dataset path', required='True', type=str, help='enter a path to a folder containing emails that you want to classify' )
    args = parser.parse_args()
    return args

def main():
    argums = create_parser() 
    read_train = corpus.read_dataset(argums.train_dataset)
    read_test = corpus.read_dataset(argums.test_dataset)
    #for the user emails I iterate over their content and read it with read_file method 
    read_usermails = corpus.read_file(argums.diremails_classify)
    spam_filter = SpamFilter()
    spam_filter.train(read_train)

#i iterate over the content of the mail in the test dataset and classify them
    for mail, label in read_test:
        result = spam_filter.classify(mail)
        #I apply precision and recall 






#opening a file for writing the classification results
#do I have to require as a condition that it is a txt file?
    with open(argums.resultfile, "w") as final_file: 
        for mail, label in read_usermails:
            result = spam_filter.classify(mail)
            final_file.write(result, label)
            #do I want to write accuracy?

 
if __name__ == "__main__":
    main()