#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import csv
import re

#takes packing angles and creates dictionary
reader = csv.reader(open('packingAngleOutput.csv', 'r'))
ab_angle_dict = {}
for row in reader:
   k, v = row
   ab_angle_dict[k] = v


with open('modified_free_complex_list.txt') as f:
    free_complex_str = f.read()

#modifies the modified free complex list ready for analysis
free_complex_str = free_complex_str.split('\n')
free_complex_str = ([s.replace('[', '') for s in free_complex_str])
free_complex_str = ([s.replace(']', '') for s in free_complex_str])
free_complex_str = ([s.replace("'", "") for s in free_complex_str])
free_complex_str = ([s.replace(', ', ': ') for s in free_complex_str])

#splits the free and complex antibodies into two list maintaining the position
#of each pair so free[0] is the same antibody as comp[0]
free_complex_lst = [x for x in free_complex_str if x ]
join_list_comp = []
join_list_free = []
for i in free_complex_lst:
   non_complexed = re.findall(r'.*(?=:)', i)      
   complexed = re.findall(r'(?<=:).*', i)
   join_list_comp.append(complexed)
   join_list_free.append(non_complexed)

#uses dictionary from abpackingangleExecute to find the angles for all free and
#complexed pdb codes
comp_angle_list = []
for i in join_list_comp:
   lx = []
   for s in i:
      s1 = s.split(' ')
      for x in s1:
         if x == '':
            pass
         else:
            try:
               lx.append(ab_angle_dict[x])
            except:
               pass
   comp_angle_list.append(lx)

free_angle_list = []
for i in join_list_free:
   lx = []
   for s in i:
      s1 = s.split(' ')
      for x in s1:
         if x == '':
            pass
         else:
            try:
               lx.append(ab_angle_dict[x])
            except:
               pass
   free_angle_list.append(lx)


#organises the data into floats
comp_float_list = []
for i in comp_angle_list:
    lt = []
    for s in i:
        lt.append(float(s))
    comp_float_list.append(lt)

free_float_list = []
for i in free_angle_list:
    lt = []
    for s in i:
        lt.append(float(s))
    free_float_list.append(lt)


#calculates the sd variation for each set of antibodies
comp_sd_varience = []
for i in comp_float_list:
   sd = np.std(i)
   comp_sd_varience += [sd]

free_sd_varience = []
for i in free_float_list:
   sd = np.std(i)
   free_sd_varience += [sd]

#calculates whether the average complex antibody angle falls within the range of
#of angles of the free form antibodies
free_varience_list = []
count = 0
true_count = 0
false_count = 0
for i in free_float_list:
   max_angle = max(i)
   min_angle = min(i)
   avg_angle = np.mean(comp_float_list[count])
   if avg_angle > min_angle and avg_angle < max_angle:
      true_count += 1
   else:
      false_count += 1
   count += 1

#Performs t-test on the angles of the free and complex antibody groups

joined_comp_angle_list = [j for i in comp_float_list for j in i]
joined_free_angle_list = [j for i in free_float_list for j in i]

total_pdb_codes = len(joined_comp_angle_list + joined_free_angle_list)

t, p = stats.ttest_ind(joined_comp_angle_list,joined_free_angle_list)
print("t-value = " + str(t))
print("p-value = " + str(p))

#Performs chi squared test on whether the average complex angle falls within
#range of the free anlges

length = len(free_complex_lst)
expected = length / 2
chi, p = stats.chisquare(true_count, f_exp=expected, ddof=1)

print("chi-square value = " + str(chi))


#Calculates the number of antibodies where the average complex angle falls
#within the range of angles of the free form antibodies


print(true_count,"/",length)

plt.figure(1)
plt.hist(free_sd_varience)
plt.ylabel('Frequency of antibody groups')
plt.xlabel('Standard deviation within antibody group')
plt.figure(2)
plt.hist(comp_sd_varience)
plt.ylabel('Frequency of antibody groups')
plt.xlabel('Standard deviation within antibody group')
plt.figure(3)
plt.scatter(free_sd_varience, comp_sd_varience)
plt.xlabel('Standard deviation of free form of antibody')
plt.ylabel('Standard deviation of complex form of antibody')
legend = plt.legend()
plt.show([1,2,3])



