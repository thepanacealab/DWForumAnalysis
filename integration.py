from os import listdir,mkdir
from os.path import isfile, join,isdir
import csv
import sys

dirs = [[f,'Forum_Data/'+f] for f in listdir('Forum_Data') if isdir('Forum_Data/'+f)]
#dirs=[['havanaabsolem-forums','Forum_Data/havanaabsolem-forums']]
print(len(dirs))
#x = int(input('Enter a number: '))
root = 'Posts'
if not isdir(root):
	mkdir(root)

general_file = root+'/' + 'statistics.tsv'
stat_file= open(general_file,'a+',newline='')
stat_Table= csv.writer(stat_file,delimiter='\t')
stat_Table.writerow(['forum name','duplicate#','Non-duplicate#'])
total1 = 0
total2 = 0
csv.field_size_limit(sys.maxsize)
print(sys.maxsize)
for direction in dirs:
	new_dir=root+'/' + direction[0]
	if not isdir(new_dir):
		mkdir(new_dir)
	files = [direction[1]+'/'+f for f in listdir(direction[1]) if isfile(direction[1]+'/'+f)]
	new_file = new_dir+'/' + 'duplicate_post.tsv'
	Post_file= open(new_file,'w',newline='')
	Post_Table= csv.writer(Post_file,delimiter='\t')
	Post_Table.writerow(['Content','username'])
	posts = []
	
	#print(direction,files)
	
	for file in files:
		input_file = open(file)
		tsv_file = csv.reader(input_file, delimiter='\t')
		j = 0
		for row in tsv_file:
			if j == 0:
				j = j +1
				continue
			Post_Table.writerow(row)
			posts.append(row[0])	
	Post_file.close()
	len1= len(posts)
	seen = list(set(posts))
	len2= len(seen)
	print(direction[0], len1, len2)
	
	total1 = total1 + len1
	total2 = total2 + len2
	stat_Table.writerow([direction[0],len1,len2])
	stat_file.flush()
	new_file = new_dir+'/' + 'No_duplicate_post.tsv'
	Post_file = open(new_file,'w',newline='')
	Post_Table = csv.writer(Post_file,delimiter='\t')
	Post_Table.writerow(['Content'])
	for post in seen:
		Post_Table.writerow([post])
	Post_file.close()

stat_Table.writerow(['sum',total1,total2])
stat_file.close()		
