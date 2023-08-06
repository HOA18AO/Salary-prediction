import csv
import re

fi = open("itviecData.csv", "r", encoding='utf-8')
read = csv.DictReader(fi, delimiter=';')
f = open("skillsFromItviec.txt", "w", encoding='utf-8')

skills_list = []
for row in read:
    skills = row['SKILLS'].split('|')
    for i in skills:
        if i not in skills_list:
            skills_list.append(i)
            f.writelines(i+'\n')
print(skills_list)
#print(len(skills_list))
f.close()
fi.close()




