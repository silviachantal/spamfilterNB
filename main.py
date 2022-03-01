#the hitchikers guide to pyhton 
#https://python-docs.readthedocs.io/en/latest/writing/structure.html
#chapter 4: strcturing your code(p65)

#this module "main.py" is the abstraction layer of the project that handles interfacing with user actions
#i will hence import my project's internal modules

#command-line application 
#i will use argparse library because it is in the Python's standard library

import argparse

def get_parser():
    parser = argparse.ArgumentParser(description="filters email contents dividing them into two categories: ham or spam") #the parser will hold all the information necessary to parse the command-line into python datatypes
    parser.add_argument('test dataset', metavar='dataset path', type=str, help='enter a path to a dataset of emails') #we define which arguments the program will require: we tell how to take strings in CLI and turn them into objects
    parser.add_argument()
    parser.add_argument()
    parser.add_argument()
    parser.add_argument()
