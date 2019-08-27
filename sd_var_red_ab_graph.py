#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import re

with open ('modified_redundant_ab_list.txt', 'r') as f:
    mod_red_ab=f.read()
    final_red_ab= mod_red_ab.translate({ord(i): None for i in "[]''"})

reader = csv.reader(open('packingAngleOutput.csv', 'r'))
ab_angle_dict = {}
for row in reader:
   k, v = row
   ab_angle_dict[k] = v

#modifying final_red_ab into a list of lists and removing blank lists while
#keeping the pdb codes in their redundant groups 
final_red_ab = final_red_ab.split('\n')
temp = []  
final_red_ab_mod = []  
for elem in final_red_ab: 
    temp2 = elem.split(', ') 
    temp.append((temp2)) 
for elem in temp: 
    temp3 = [] 
    for elem2 in elem: 
        temp3.append(elem2) 
    final_red_ab_mod.append(temp3)

final_red_ab_mod = [x for x in final_red_ab_mod if x != ['']]

#uses the dictionary from ab_packingangle_execute to create a list of angles
#once again keeping the codes in their redundant groups
angle_list = []
for i in final_red_ab_mod:
    lx = []
    for s in i:
        try:
            if ab_angle_dict[s]:
               lx.append(ab_angle_dict[s])
        except KeyError:
            pass
    angle_list.append(lx)
#converts angles strings into floats
float_list = []
for i in angle_list:
    lt = []
    for s in i:
        lt.append(float(s))
    float_list.append(lt)

#removes any empty lists
float_list = [x for x in float_list if x != []]

sd_varience = []
for i in float_list:
   sd = np.std(i)
   sd_varience += [sd]

varience_list = []
for i in float_list:
   varience = (max(i)-min(i))
   varience_list += [varience]


m = max(sd_varience)
print(m)
loc_max =[i for i, j in enumerate(sd_varience) if j ==m]
loc_max = str(loc_max)
loc_max = loc_max.replace('[','')
loc_max = loc_max.replace(']','')
loc_max = int(loc_max)
max_sd_var = float_list[loc_max]
max_var_sd_pdb = ''
for i in max_sd_var:
    for k, v in ab_angle_dict.items():
        i = str(i)
        if v == i:
            max_var_sd_pdb += k + ', '
print("PDB codes of antibody with the highest standard deviation =",max_var_sd_pdb)

n = min(sd_varience)
print(n)
loc_min =[i for i, j in enumerate(sd_varience) if j ==n]
loc_min = str(loc_min)
loc_min = loc_min.replace('[','')
loc_min = loc_min.replace(']','')
loc_min = int(loc_min)
min_sd_var = float_list[loc_min]
min_var_sd_pdb = ''
for i in min_sd_var:
    for k, v in ab_angle_dict.items():
        i = str(i)
        if v == i:
            min_var_sd_pdb += k + ', '
print("PDB codes of antibody with the lowest standard deviation =",min_var_sd_pdb)

print("Highest standard deviation in single redundant antibody group =", m)

plt.hist(sd_varience)
plt.ylabel('Frequency of antibody groups')
plt.xlabel('Standard deviation within each antibody group')

plt.show()
