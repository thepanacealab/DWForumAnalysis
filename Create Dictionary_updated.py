import csv
import re

def formart1(mapTerm):
	maps=set()
	parentheses = re.findall(r" ?\([^)]+\)",mapTerm)
	if len(parentheses)>0:
		mapTerm = re.sub(r" ?\([^)]+\)",'',mapTerm)
		for p in parentheses:
			phrase = p[1:-2]
			parts = phrase.split(',')
			for part in parts:
				maps.add(re.sub('[^0-9a-zA-Z ]+', '', part.strip()))
	parts= re.split(',|/|;', mapTerm) 	
	for part in parts:
		elements = re.split('and|or', (re.sub('[^0-9a-zA-Z ]+', '', part.strip())))
		for element in elements:
			if(len(element.strip())>0):
				maps.add(element.strip())
	return list(maps)

def formart2(mapTerm):
	maps=set()

	isomer = re.findall(r" ?\(positional isomer.*",mapTerm)
	if len(isomer)>0:
		raw = isomer[0][20:-2].replace(':','').strip()
		mapTerm = re.sub(r"\(positional isomer.*",'',mapTerm)
		parts= re.split(', |; ', raw)
		for part in parts:
			if(len(part.strip())>0):
				maps.add(part.strip())

	parts= re.split(', |; ', mapTerm)
	for part in parts:
		if(len(part)>0):
			elements= re.split('and|or', part)
			for element in elements:
				if(len(element.strip())>0):
					maps.add(element.strip())			

	return list(maps)

def write_result_DEA(slangs,maps,dictionary,sign):
	global tsv_output, Customized_Drug_Dictionary, ID,standard
	num  = 0

	for term in maps:
		term = term.lower()
		if term not in standard and term not in dictionary and len(term) > 3:
			tsv_output.writerow([ID, term, 'DEA('+sign+')'])
			dictionary[term] = ID
			ID = ID + 1
			num = num + 1

	for slang in slangs:
		slang = slang.lower()
		if slang not in standard and slang not in dictionary and len(slang) > 3:
			tsv_output.writerow([ID, slang, 'DEA('+sign+')'])
			dictionary[slang] = ID
			ID = ID + 1
			num = num + 1
		for term in maps:
			if len(slang)>3: 
				term = term.lower()
				Customized_Drug_Dictionary.writerow([ID, slang, 'DEA('+sign+')', term])
				ID = ID + 1 

	return dictionary, num

outputFile = open('Drug_Dictionary.tsv', 'w', newline='', encoding='utf-8')
tsv_output = csv.writer(outputFile, delimiter='\t')
tsv_output.writerow(['TermID (RxCUI)', 'Term', 'Source'])
ID = 1
number = 0

Customized_Drug_DictionaryFile = open('Customized_Drug_Dictionary.tsv', 'w', newline='', encoding='utf-8')
Customized_Drug_Dictionary = csv.writer(Customized_Drug_DictionaryFile, delimiter='\t')
Customized_Drug_Dictionary.writerow(['TermID (RxCUI)', 'Term', 'Source', 'MapsTo'])

ID = 1
number = 0

#########read standard dictionary#######################
input_standard = open('standard_RxNorm_dictionary.csv')
csv_standard = csv.reader(input_standard,delimiter='\t')
standard= {}
j=0
for line in csv_standard:
	if j == 0:
		j = j +1
		continue
	if line[4].lower() not in standard:
		standard[line[4].lower()]= str('C'+line[0])
		tsv_output.writerow(['C'+line[0], line[4].lower(), 'RxNorm'])
		Customized_Drug_Dictionary.writerow(['C'+line[0], line[4].lower(), 'RxNorm',''])
		number = number + 1
input_standard.close()
print('RxNorm',number)
xxx = number
#########read Controlled dictionary######################
input_Controlled = open('Controlled_Substances.csv')
csv_Controlled = csv.reader(input_Controlled,delimiter='\t')
Controlled= {}
total=0
j=0
for line in csv_Controlled:
	if j == 0:
		j = j +1
		continue
	mapTerm = line[4].strip()
	Term = line[0].strip() #standard
	maps = [Term]
	#if len(Term)<4:
	#	continue		
	slangs = formart2(mapTerm) #slang: empty
	[Controlled, number]= write_result_DEA(slangs,maps,Controlled,'Controlled')
	total = total + number
print('Controlled',total)
input_Controlled.close()

#########read Slang dictionary###########################
input_Slang = open('Drug_Slang.csv')
csv_Slang = csv.reader(input_Slang,delimiter='\t')
Slang= {}
#total=0
j=0
for line in csv_Slang:
	if j == 0:
		j = j +1
		continue
	mapTerm = line[1].strip()
	slangs = [line[0].strip()] #slang
	maps =formart1(mapTerm) #standard
	[Controlled, number]= write_result_DEA(slangs,maps,Controlled,'Slang')
	total = total + number
print('Slang',total)
input_Slang.close()

#########read street dictionary##########################
input_street = open('Drug_street_name.csv')
csv_street = csv.reader(input_street,delimiter='\t')
street= {}
#total=0
j=0
for line in csv_street:
	if j == 0:
		j = j +1
		continue
	Term = line[0].strip().lower().replace('\r',' ').replace('\n',' ') #standard
	maps = [Term]
	#if len(Term)<4:
	#	continue
	mapTerm = line[1].strip().lower().replace('\r',' ').replace('\n',' ') #slang: empty
	slangs =formart1(mapTerm)
	[Controlled, number]= write_result_DEA(slangs,maps,Controlled,'Street')
	total = total + number
print('Street',total)
input_street.close()
print(xxx + total)
outputFile.close()
Customized_Drug_DictionaryFile.close()
#unfoundedTermFile.close()
#unfoundedTermMaptoTermFile.close()

