import csv

outfile = open("discord_corpus.txt","a")
for line in open("all_chats.csv"):
	cols = line.split(",")
	message = cols[3]
	outfile.write(message + "\n")

outfile.close()