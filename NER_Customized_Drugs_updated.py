from spacy.lang.en import English
from spacy.pipeline import EntityRuler
import csv
import spacy
import glob
import os
import argparse
import pickle
import ast 
import sys

csv.field_size_limit(sys.maxsize)

input_standard = open('dictionary_jmb.tsv')
dictionary_file = csv.reader(input_standard,delimiter='\t')

vocab = {}
counts={}
i = 0
for product in dictionary_file:
	if i ==0:
		i = i +1
		continue
	vocab[product[1]]= product[0]
	counts[product[1]] = 0		
input_standard.close()

patterns = []
for key in vocab:
	patterns.append({"label":vocab[key],"pattern":key})
print(len(patterns))

nlp = English()
ruler = EntityRuler(nlp)

ruler.add_patterns(patterns)
nlp.add_pipe(ruler)


products_raw = open('all_post.tsv')
products = csv.reader(products_raw,delimiter='\t')

Posts={}
annoPosts={}
i = 0
for product in products:
	if i ==0:
		i = i +1
		continue
	description = product[1].lower()
	if product[0] in Posts:
		Posts[product[0]] +=1
	else:
		Posts[product[0]] =1
		annoPosts[product[0]] =0
	desc = nlp(description)
	if len(desc.ents)>0:
		annoPosts[product[0]] +=1	

	for ent in desc.ents:
		if ent.text in counts:
			counts[ent.text] +=1
		#else:
		#	print(ent.text)
	i = i+1
	if i % 10000 == 0:
		print(i)
	#if i>20000:
	#	break
products_raw.close()

all_vocab_file = open('all_vocab.tsv','w',newline='')
all_vocab= csv.writer(all_vocab_file,delimiter='\t')
all_vocab.writerow(['TermID','Term','Counts'])

for item in counts:
	all_vocab.writerow([vocab[item],item,counts[item]])
all_vocab_file.close()

annotatedPosts_file = open('annotatedPosts.tsv','w',newline='')
annotatedPosts= csv.writer(annotatedPosts_file,delimiter='\t')
annotatedPosts.writerow(['forum name','annotated posts #','total posts #',"annotated posts percent"])

Ps = 0
aPs = 0
for item in Posts:
	Ps += Posts[item]
	aPs += annoPosts[item]
	annotatedPosts.writerow([item,str(annoPosts[item]),str(Posts[item]),str(100*annoPosts[item]/Posts[item])])
annotatedPosts.writerow(["SUM",str(aPs),str(Ps),str(100*aPs/Ps)])
annotatedPosts_file.close()

