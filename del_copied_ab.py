#!/usr/bin/env python3

import re
#takes the redundant_ab.txt document produced by a previous script and takes all PDB
#codes which use the first biological conformation in the pdb file to remove the
#duplicated biological conformations 
with open ('redundant_ab.txt', 'r') as f:
    red_ab_list = f.readlines()
lastPDB = ''
output =''
for lines in red_ab_list:
    items = lines.split('\n')
    items.remove('')
    new_items = [word for line in items for word in line.split(', ')]
    for pdb in new_items:
        pdb.strip(",")
        pdbcode = pdb[:4]
        if pdbcode == lastPDB:
            pass
        else:
            output += pdb + ', '
        lastPDB = pdbcode
    output += '\n'

output = output.split("\n")

output = [i.replace(',','') for i in output]
output = [i.replace(',,','') for i in output]
output = [i.replace(' ',',') for i in output]
final_output = []
while('' in output):
    output.remove('')
output = [[i] for i in output]

final_output = [item[0].split(',') for item in output]
final_output = [' '.join(i).split() for i in final_output]
# This next line removes all the lines which are no longer redundant due to having only
#1 or no PDB files in the list
mod_red_ab_list = [x for x in final_output if len(x) > 1]
#prints the amount of redundant groups left in the dataset
count = 0
count = len(mod_red_ab_list)
print("Total redundant antibody groups=" ,count)
#prints the amount of pdb files in the dataset
count = 0
for x in mod_red_ab_list:
    count+= len(x)
print("Total PDB files=",count)

with open("modified_redundant_ab_list.txt", 'w') as f:
     for line in mod_red_ab_list:
          f.write(str(line) + '\n')


