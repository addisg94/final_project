#!/usr/bin/env python3

import re
#takes the redundant_ab.txt document produced by a previous script and takes all PDB
#codes which use the first biological conformation in the pdb file to remove the
#duplicated biological conformations 
with open('FreeAntibody_AntibodyAntigen.txt', 'r') as f:
    free_complex_str = f.read().splitlines()
lastPDB = ''
output =''
for lines in free_complex_str:
    new_items = lines.split(', ')
    for pdb in new_items:
        pdb = pdb.split(':')
        for i in pdb:
            i = i.split(',')
            for x in i:
                pdbcode = x[:4]
                if pdbcode == lastPDB:
                    pass
                else:
                    list(x)
                    output += x + ' '
                lastPDB = pdbcode
            output += '\n'
output = output.split("\n")

count = 0
free = ''
comp = ''

for line in output:
    if (count % 2) == 0:
        free += line + '\n'
    else:
        comp += line + '\n'
    count += 1
free = free.split('\n')
free = tuple(free)
comp = comp.split('\n')
comp = tuple(comp)

free_comp = list(zip(free, comp))

new_free_comp = []
for i in free_comp:
    if '' in i:
        pass
    else:
        new_free_comp.append(i)

fin_free_comp = []
for i in new_free_comp:
    if len(i[0]) > 7 and len(i[1]) > 7:
        fin_free_comp.append(i)

fin_free_comp = tuple(tuple(b.strip() for b in a) for a in fin_free_comp)
fin_free_comp = [list(elem) for elem in fin_free_comp]
    
count = 0
count = len(fin_free_comp)
print("Total redundant free and complex antibody groups=" ,count)

with open("modified_free_complex_list.txt", 'w') as f:
     for line in fin_free_comp:
         f.write(str(line) + '\n')
