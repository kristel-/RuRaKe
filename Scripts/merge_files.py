#Script that merges two tables based on the value
#Eleri Aedmaa
#Causing some blemishes

import sys
import re
file1 = open('fail_1.txt', 'r') #Reading the first file/table.
file2 = open('fail_2.txt', 'r') #Reading the second file/table.
vahepealne = open('vahepealne.txt', 'w') #Writing output file.
koos = open('koos.txt', 'w') #Writing output file.
puhas = open('puhas.txt', 'w') #Writing output file.

list1=[] #List for the second file.
list2=[] #List for the first file.

loplik=[] #List for merged files.

#The content of the first file will be in the list_2, one word = one list member.
for i in file1: 
    j= i.split()
    list2.append(j)

#The content of the first file will be in the list_1, one word = one list member.
for i in file2: 
    j= i.split()
    list1.append(j)

#print(list2)
#print(list1)

#Closing files
file1.close()
file2.close()


for i in list1: #Sentence from list_1
    for j in list2: #Sentence from list_2
        if j[0]==i[3]: #If words are the same, then they are written to the list 'loplik'.
            loplik.append(i + j)
    else:
        loplik.append(i) #All the members from the list_1 are written to list 'loplik'.


for i in loplik: #Every sentence from list 'loplik' are written to separate line.
    koos.write(str(i) +'\n')
           
koos.close() #File closed.

#Removing unnecessary symbols
lopp=open('koos.txt', 'r')
for i in lopp:
    ilma=re.sub('[\'\],\[]', '', i)
#    print(puhas)
    puhas.write(ilma)

#Closing files
lopp.close()
puhas.close()



