import os

stopwords_filename = "stopwords.txt"
transcripts_dir = "./transcripts/"
word_dict = {}

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
    if word.find("-") >= 0:
        return True
    if word.find("'") >= 0:
        return True
    if word.find(",") >= 0:
        return True
    return False

def afterProcessing(word):
    index1 = word.find("-")
    index2 = word.find("\'")
    index3 = word.find(",")
    temp = set()
    if index1 >= 0:
        temp.add(index1)
    if index2 >= 0:
        temp.add(index2)
    if index3 >= 0:
        temp.add(index3)
    
    index = min(temp)
    return word[:index].lower()

def findOnlyOccurOnceWord():
    count = 0
    for word, freq in word_dict.items():
        if freq == 1:
            count += 1

    return count

def main():
    checkFileExist(stopwords_filename)
    stopwords = createStopwordsSet(stopwords_filename)

    checkDirExist(transcripts_dir)
    words_before_processing = 0
    words_after_processing = 0

    for filename in os.listdir(transcripts_dir):
        filename = transcripts_dir + filename

        with open(filename) as f:
            for line in f:
                words = line.split()

                for word in words:
                    words_before_processing += 1

                    if word not in stopwords:
                        if needProcess(word):
                            word = afterProcessing(word)
                    
                            if word not in stopwords and word != "":
                                words_after_processing += 1
                                if word_dict.get(word) == None:
                                    word_dict[word] = 0
                                word_dict[word] += 1


    print "The number of word tokens in the database (before: " + str(words_before_processing) +  " words, after text processing: " +str(words_after_processing) + " words.)"
    print "The number of unique words in the database: " + str(len(word_dict))
    only_occur_once = findOnlyOccurOnceWord()
    print "The number of words that occur only once in the database " + str(only_occur_once)

if __name__ == '__main__':
    main()
    
