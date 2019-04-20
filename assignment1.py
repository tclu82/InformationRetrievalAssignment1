import os

stopwords_filename = "stopwords.txt"
transcripts_dir = "./transcripts/"

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

def afterProcessing(word):



    return word

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
                        word = afterProcessing(word)
                        words_after_processing += 1

    # temp = "You're cool"
    # index = temp.find("'")
    # print (index)
    # print (temp[:index])

    print "The number of word tokens in the database (before: " + str(words_before_processing) +  " words, after text processing: " +str(words_after_processing) + " words.)"

if __name__ == '__main__':
    main()
