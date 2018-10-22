import sqlite3
conn = sqlite3.connect('../../wordforms.db')

c = conn.cursor()
#c.execute('''CREATE TABLE Dutch
 #        (Word Text,
  #       PhonDISC Text,
   #      PhonSylDISC Text)
# ''')


with open("Dutch.txt") as f:
    content = f.readlines()

content = [x.strip() for x in content]
content = [x.split("\\") for x in content]

remove_lonesome = []
for phrase in content:
    if(phrase[1] != '' and phrase[2] != ''):
        remove_lonesome.append(phrase)

index_list = []

intervals = 500
for elt in range(0,len(remove_lonesome), intervals):
    index_list.append((elt, elt + intervals))

tmp = index_list[-1][0]
index_list.pop()
index_list.append((tmp, len(remove_lonesome)-1))

query_string = """INSERT INTO Dutch(Word, PhonDISC, PhonSylDISC)
VALUES(?,?,?)"""

fixed_list = []
count = 0
for entry in remove_lonesome:

    if(len(entry) != 3):
        count+=1
        print entry
    else:
        fixed_list.append(entry)
print count
c.executemany(query_string, fixed_list)
conn.commit()
