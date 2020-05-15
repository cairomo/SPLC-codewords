"""
cairo mo, CS 184
merge discord chats into 1 csv
"""
import csv
import glob
import os
from os import listdir
from os.path import isfile, join

outfile = open("all_chats.csv","a")

# get all files in folder
filenames = []
for f in glob.glob("*.csv"):
	filenames.append(f)

# write first file, including header
sep = ","
firstline = True
for line in open(filenames[0]):
	if firstline:
		outfile.write("User ID,Username,Message ID, Message Content,Server Name\n")
		# outfile.write(line[:-1] + ",Server Name\n") # add Server Name as a column
		firstline = False
	else:
		cols = line.split(",")
		if len(cols) == 6 and len(cols[5][:-1]) != 0: # if less than 6 then message text is empty
			out_line = sep.join((cols[1], cols[2], cols[4], cols[5][:-1], filenames[0]))
			outfile.write(out_line + "\n")
		#outfile.write(line[:-1] + filenames[0] + "\n")

# write the rest of the files
for f in filenames[1:]:
	infile = open(f)
	infile.__next__() # skip header
	for line in infile:
		cols = line.split(",")
		if len(cols) == 6 and len(cols[5][:-1]) != 0: # message content not empty
			out_line = sep.join((cols[1], cols[2], cols[4], cols[5][:-1], f))
			outfile.write(out_line + "\n")
			# outfile.write(line[:-1] + f + "\n")
			# pdb.set_trace()
	infile.close()

outfile.close()
