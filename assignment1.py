import os
import unicodedata
from sys import maxsize

stopwords_filename = "stopwords.txt"
transcripts_dir = "./transcripts/"
word_dict = {}
check_set = {'-', '\'', ',', '.'}
files = 0
words_before_processing = 0
words_after_processing = 0

def checkDirExist(filename):
    if not os.path.isdir(filename):
        print("Directory doesn't exist")
        exit(1)

def checkFileExist(dirname):
    if not os.path.isfile(dirname):
        print("File doesn't exist")
        exit(1)

def createStopwordsSet(filename):
    hash_set = set()
    with open(filename) as f:
        content = f.read().splitlines()
        for line in content:
            hash_set.add(line)
    return hash_set

def needProcess(word):
    for char in check_set:
        if word.find(char) >= 0:
            return True
    return False

def afterProcessing(word):
    index = maxsize
    for char in check_set:
        if word.find(char) >= 0:
            index = min(index, word.find(char))
    return word[:index].lower()

def findOnlyOccurOnceWord():
    count = 0
    for word in word_dict:
        if word_dict[word] == 1:
            count += 1
    return count

def buildDictionary(dir, stopwords):
    for filename in os.listdir(dir):
        global files
        files += 1
        filename = transcripts_dir + filename
        try:
            # Avoid UnicodeDecodeError: 'utf-8' codec can't decode byte
            with open(filename, encoding = "ISO-8859-1") as f:
                data = f.read()
                words = data.split()
                for word in words:
                    global words_before_processing
                    words_before_processing += 1
                    if word not in stopwords:
                        if needProcess(word):
                            word = afterProcessing(word)
                            if word not in stopwords and word != "":
                                global words_after_processing
                                words_after_processing += 1
                                if word_dict.get(word) == None:
                                    word_dict[word] = 0
                                word_dict[word] += 1
        except OSError:
            print(OSError)

def findTopKFreqencyWords(K):
    top_k_dict = {}


    return top_k_dict

def main():
    checkFileExist(stopwords_filename)
    stopwords = createStopwordsSet(stopwords_filename)
    checkDirExist(transcripts_dir)
    buildDictionary(transcripts_dir, stopwords)

    print ("The number of word tokens in the database (before: " + str(words_before_processing) +  " words, after text processing: " +str(words_after_processing) + " words.)")
    print ("The number of unique words in the database: " + str(len(word_dict)))
    only_occur_once = findOnlyOccurOnceWord()
    print ("The number of words that occur only once in the database " + str(only_occur_once))
    print ("The average number of word tokens per document: " + str(words_before_processing / files))
    
    top_k_dict = findTopKFreqencyWords(30)

if __name__ == "__main__":
    main()