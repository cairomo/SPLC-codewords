# Implements word2vec, reads files, and then runs k-means

import collections
import k_means
import csv
import nltk
import warnings
import logging
import gensim
import time
import json

warnings.filterwarnings(action='ignore')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

messages = []

def run_algorithm(chat_file, chat_file_2, codeword_file):
    # reads two input files with different formats as corpus
    read_file_full(messages, chat_file)
    read_file_sorted(messages, chat_file_2)
    logging.info("Read Messages")
    model = gensim.models.Word2Vec(messages, size=150, window=10, min_count=4, workers=10)
    model.train(messages, total_examples=len(messages), epochs=10)
    time.sleep(2)  # KeyedVectors Instance gets stored
    words = [key for key in model.wv.vocab.keys()]
    vecs = [model.wv.word_vec(word) for word in words]
    codewords = read_codewords(codeword_file)
# arbitrarily runs k-means three times to compare results. 250 centroids, 25 max iterations
    for i in range(3):
        centers, assignments, score = k_means.kmeans(vecs, words, codewords, 250, 25)
        analyze(words, assignments, score, i)

# uploads resultant clusters to new text file, along with error score
def analyze(words, assignments, score, i):
    clusters = collections.defaultdict(list)
    for x in range(len(assignments)):
        clusters[assignments[x]].append(words[x])
    my_json_string = json.dumps(clusters)
    print(score)
    if i == 0:
        text_file = open("results.txt", "w")
        n = text_file.write(my_json_string)
        text_file.close()
    else:
        text_file = open("results.txt", "a")
        n = text_file.write(my_json_string)
        text_file.close()

# reads file that has info on usernames, channel, etc. but we only want the messages
def read_file_full(messages, filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in csv_reader:
            messages.append(nltk.word_tokenize(row[len(row) - 2].lower()))
#            messages.append(gensim.utils.simple_preprocess(row[len(row)-2]))


# reads file that has been parsed to only have the desired messages
def read_file_sorted(messages, filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, quoting=csv.QUOTE_NONE)
        for row in csv_reader:
            if row:
                messages.append(nltk.word_tokenize(row[0].lower()))
#            messages.append(gensim.utils.simple_preprocess(row[len(row)-2]))


# reads a csv file of known codewords
def read_codewords(codeword_file):
    codewords = []
    with open(codeword_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            wordlist = nltk.word_tokenize(row[0].lower())
            for word in wordlist:
                if word != "and" and word != "of" and word != "the" and word not in codewords:
                    codewords.append(word)
    return codewords

# runs algorithms on our given codewords, with two distinct leaked discord corpuses
run_algorithm('all_chats_discord_1.csv', 'discord_corpus', 'codewords.csv')
