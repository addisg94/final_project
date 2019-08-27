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

#calculates the varience for each redundant group using min and max
varience_list = []
for i in float_list:
   varience = (max(i)-min(i))
   varience_list += [varience]

mean_var = []
for i in float_list:
    mean = np.mean(i)
    mean_var += [mean]
    
tot_mean_var = np.mean(varience_list)
print(tot_mean_var)



x = (max(varience_list))
var_max =[i for i, j in enumerate(varience_list) if j ==x]
var_max = str(var_max)
var_max = var_max.replace('[','')
var_max = var_max.replace(']','')
var_max = int(var_max)
max_var = float_list[var_max]
max_var_pdb = ''
for i in max_var:
    for k, v in ab_angle_dict.items():
        i = str(i)
        if v == i:
            max_var_pdb += k + ', '
print("PDB codes of redundant antibody group with largest variation in angle =" ,max_var_pdb)
print(x)
z = (min(varience_list))
var_min =[i for i, j in enumerate(varience_list) if j ==z]
var_min = str(var_min)
var_min = var_min.replace('[','')
var_min = var_min.replace(']','')
var_min = int(var_min)
min_var = float_list[var_min]
min_var_pdb = ''
for i in min_var:
    for k, v in ab_angle_dict.items():
        i = str(i)
        if v == i:
            min_var_pdb += k + ', '
print("PDB codes of redundant antibody group with smallest variation in angle =" ,min_var_pdb)
count = 0
for i in varience_list:
   if i > 6:
      count += 1
print("number of antibody groups with a degree of variation greater than 6 degrees=", count)
plt.hist(varience_list)
plt.xlabel('Difference in degrees between minimum and maximum angle')
plt.ylabel('Frequency of antibody groups')
plt.show()
