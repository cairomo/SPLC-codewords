# cairo mo
import csv
import nltk
import os
import pdb

def generate_corpus():
	outfile = open("discord_corpus.txt","a")
	for line in open("all_chats.csv"):
		cols = line.split(",")
		message = cols[3]
		outfile.write(message + "\n")

	outfile.close()

# generate_corpus()

f = open('discord_corpus.txt')
raw = f.read()

tokens = nltk.word_tokenize(raw)

f_twitter = open('normal_twitter_corpus.txt')
raw_twitter = f_twitter.read()

tokens_twitter = nltk.word_tokenize(raw_twitter)

#Create your bigrams
def generate_bigram_frequency():
	bgs = nltk.bigrams(tokens)

	#compute frequency distribution for all the bigrams in the text
	fdist = nltk.FreqDist(bgs)

	bigrams = sorted(fdist, key=fdist.get, reverse=True)
	freqs = sorted(fdist.values(), reverse=True)

	return bigrams, freqs

def write_bigrams(bigrams, freqs):
	outfile = open("bigrams.csv","a")
	counter = 0
	for counter in range(len(bigrams)):
		#pdb.set_trace()
		outfile.write(','.join(bigrams[counter]) + "," + str(freqs[counter]) + "\n")

	outfile.close()

def generate_word_frequency():
	fdist = nltk.FreqDist(tokens)
	unigrams = sorted(fdist, key=fdist.get, reverse=True)
	freqs = sorted(fdist.values(), reverse=True)
	return unigrams, freqs

def write_unigrams(unigrams, freqs):
	outfile = open("unigrams.csv","a")
	counter = 0
	for counter in range(len(unigrams)):
		#pdb.set_trace()
		outfile.write(unigrams[counter] + "," + str(freqs[counter]) + "\n")

	outfile.close()

bigrams, freqs = generate_bigram_frequency()
write_bigrams(bigrams, freqs)

unigrams, freqs = generate_word_frequency()
write_unigrams(unigrams, freqs)