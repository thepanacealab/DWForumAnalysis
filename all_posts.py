from os import listdir,mkdir
import shutil
from os.path import isfile, join,isdir
import tarfile
from bs4 import BeautifulSoup
import spacy
import csv
import sys

csv.field_size_limit(sys.maxsize)

all_post_file= open('Posts/all_post.tsv','w',newline='')
all_post= csv.writer(all_post_file,delimiter='\t')
all_post.writerow(['Forum Name','Content'])

path = 'Posts'
onlydirs = [f for f in listdir(path) if isdir(join(path, f))]

for f in onlydirs:
	file_name = path + '/' + f +'/' + 'No_duplicate_post.tsv'
	#print(file_name,f)
	#x = int(input('Enter a number: '))
	input_file = open(file_name)
	post_file = csv.reader(input_file,delimiter='\t')
	for post in post_file:
		all_post.writerow([f,post[0]])
	input_file.close()

all_post_file.close()
