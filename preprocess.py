import json
import codecs
import re
import csv
from opencc import OpenCC
cc = OpenCC('t2s')
'''
fo=codecs.open("data/anime.csv","r", "utf-8")
ls=[]
for line in fo:
    line=line.replace("\n","")
    new_line = line.split(",")
    new_line = new_line[1]
    pattern = r'第(.+?)(季|期|章|幕|届|部|话)'
    new_line = re.sub(pattern, "", new_line)
    pattern = r'(1-9)(期)'
    new_line = re.sub(pattern, "", new_line)
    ls.append(new_line)
fo.close()
fw1=codecs.open("data/anime_dict.txt","w", "utf-8")
fw2=codecs.open("data/anime.txt","w", "utf-8")
for i in range(0,len(ls)):
    fw1.write(ls[i]+ ' ' + 'nz' + '\n')
    fw2.write(ls[i]+'\n')
# fw1.close()
fw2.close()
'''

# fo=codecs.open("data/stuff.csv","r", "utf-8")
filename='data/cast.csv'
# cnt = 0
ls=[]
with open(filename) as fo:
    reader = csv.DictReader(fo)
    for row in reader:
        names = cc.convert(row['name'])
        ls.append(names)
        other_names = cc.convert(row['other names'])
        pattern = '\'(.+?)\''
        nick_names = re.findall(pattern, other_names)
        ls = ls+nick_names
        # cnt += 1
        # if cnt>5:
        #     break
        # print(ls)
# fo.close()

fw1=codecs.open("data/cast_dict.txt","w", "utf-8")
fw2=codecs.open("data/cast.txt","w", "utf-8")
for i in range(0,len(ls)):
    fw1.write(ls[i]+ ' ' + 'nz' + '\n')
    fw2.write(ls[i]+'\n')
fw2.close()

