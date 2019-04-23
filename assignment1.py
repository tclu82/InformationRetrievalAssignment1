#/usr/bin/env python

# ======================================================================================
# title           :assighment1.py
# description     :TCSS 554 Information retrieval and Search assignment 1 
# author          :Zac Lu
# date            :20190421
# version         :1.0
#
# usage           :python assignment1.py
#
# notes           :stopwords.txt and transcripts need to be downloaded for this script
# python_version  :3.7.3
# ======================================================================================

import os
import unicodedata
from sys import maxsize
import math
import re
import csv

# constants and gloabl variable
stopwords_filename = "stopwords.txt"
transcripts_dir = "./transcripts/"
term_dict = {}
check_set = {'-', '\'', ',', '.'}
files = 0
words_before_processing = 0
words_after_processing = 0

"""
Define a TermData class to store term, term frequency, document frequency.
"""
class TermData:
    def __init__(self, term, tf, df):
        self.term = term
        self.tf = tf
        self.df = df

"""
Check if file exist
"""
def checkDirExist(filename):
    if not os.path.isdir(filename):
        print("Directory doesn't exist")
        exit(1)

"""
Check if directory exist
"""
def checkFileExist(dirname):
    if not os.path.isfile(dirname):
        print("File doesn't exist")
        exit(1)

"""
Read from stopword.txt and create a set for later stopwords check
"""
def createStopwordsSet(filename):
    hash_set = set()
    with open(filename) as f:
        content = f.read().splitlines()
        for line in content:
            hash_set.add(line)
    return hash_set

"""
Find out only 1 occurance term
"""
def findOnlyOccurOnceWord():
    count = 0
    for term in term_dict:
        if term_dict[term].tf == 1:
            count += 1
    return count

"""
Use the input directory and stopword set to build the a dictory{term, term_data}
"""
def buildDictionary(dir, stopwords):
    global term_dict
    global files
    for filename in os.listdir(dir):
        files += 1
        filename = transcripts_dir + filename
        term_set = set()
        try:
            # Avoid UnicodeDecodeError: 'utf-8' codec can't decode byte
            with open(filename, encoding = "ISO-8859-1") as f:
                data = f.read()
                words = data.split()
                term_data = None

                for word in words:
                    global words_before_processing
                    words_before_processing += 1
                    global words_after_processing
                    if word == "--":
                        continue
                    word = word.lower()
                    
                    if word not in stopwords:
                        # Use regex to check if word contains [. , ']
                        match = re.match("\w+[.,\']", word)
                        if match:
                            temp_list = re.split("[.,\']", word)
                            for temp in temp_list:
                                if temp not in stopwords and temp != "":
                                    words_after_processing += 1
                                    if term_dict.get(temp) == None:
                                        term_dict[temp] = TermData(temp, 0, 0)
                                        term_data = term_dict[temp]
                                        term_data.tf += 1
                                        term_set.add(temp)
                        else:
                            # if word not in stopwords and word != "":
                            words_after_processing += 1
                            if term_dict.get(word) == None:
                                term_dict[word] = TermData(word, 0, 0)
                            term_data = term_dict[word]
                            term_data.tf += 1
                            term_set.add(word)
                
                for term in term_set:
                    term_data = term_dict[term]
                    term_data.df += 1

        except OSError:
            print(OSError)

"""
Find out top k frequency term from the term_dict
"""
def findTopKFreqencyWords(k):
    top_k_dict = {}
    freq = 0
    word = ""
    while k > 0:
        for term, term_data in term_dict.items():
            if term_data.tf > freq:
                freq = term_data.tf
                word = term   
        top_k_dict[word] = term_dict[word]
        term_dict.pop(word, None)
        freq = 0
        k -= 1
    return top_k_dict

def outputToCSV(top_k_dict):
    with open('test.csv', mode='w') as test_csv:
        csv_writer = csv.writer(test_csv, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Term','Tf','Tf(weight)','df','IDF','tf*idf','p(term)'])
        for term, term_data in top_k_dict.items():
            tf = term_data.tf
            tf_weight = 1 + math.log(tf)
            tf_weight_text = "{:.3f}".format(tf_weight)
            df = term_data.df
            idf = math.log(files / df)
            idf_text = "{:.3f}".format(idf)
            tf_idf_text = "{:.3f}".format(tf * idf)
            p_term = (tf / words_before_processing)
            p_term = "{:.3f}".format(p_term)
            csv_writer.writerow([term, tf, tf_weight_text, df, idf_text, tf_idf_text, p_term])

"""
Main funciton
"""
def main():
    checkFileExist(stopwords_filename)
    stopwords = createStopwordsSet(stopwords_filename)
    checkDirExist(transcripts_dir)
    buildDictionary(transcripts_dir, stopwords)

    print ("The number of word tokens in the database (before: " + str(words_before_processing) +  " words, after text processing: " + str(words_after_processing) + " words.)")
    print ("The number of unique words in the database: " + str(len(term_dict)))
    only_occur_once = findOnlyOccurOnceWord()
    print ("The number of words that occur only once in the database " + str(only_occur_once))
    print ("The average number of word tokens per document: " + str(words_before_processing / files))

    top_k_dict = findTopKFreqencyWords(30)
    outputToCSV(top_k_dict)
    print("For 30 most frequent words in the database:")
    print('Term\tTf\tTf(weight)\tdf\tIDF\ttf*idf\tp(term)')
    for term, term_data in top_k_dict.items():
        tf = term_data.tf
        tf_weight = 1 + math.log(tf)
        df = term_data.df
        idf = math.log(files / df)
        p_term = (tf / words_before_processing)
        print("%s\t%s\t%.2f\t\t%s\t%.2f\t%.2f\t%.3f" % (term, tf, tf_weight, df, idf, tf * idf, p_term))

if __name__ == "__main__":
    main()