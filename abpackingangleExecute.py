#!/usr/bin/env python3
import subprocess
import re
import csv

pdb_file_loc = "~/project/LH_Combined_Martin/"

#open modified redundant ab list from del copied ab and delete excess characters
with open ('redundant_antibody_list.txt', 'r') as f:
    mod_red_ab=f.read()
    red_ab_string= mod_red_ab.translate({ord(i): None for i in "[]''"})

red_ab_list = red_ab_string.split()
red_ab_list = ([s.replace(',', '') for s in red_ab_list])

final_output = ""
#execute abpackingangle for all pdb codes in red_ab_list removing all pdb codes
#which have too large a distance between VH and VL
for i in red_ab_list:
    try:
        xe = "~/bin/abpackingangle -q -p " +i +" " +pdb_file_loc+i+ ".pdb"
        output = subprocess.check_output(xe, shell=True)
        output = str(output, 'utf-8')          
        if re.search(r'\w\w\w\w_\w:\s-\d\d\.\d\d\d\d\d\d', output):
            final_output += output
        else:
            pass
    except:
        pass

reg_2 = re.compile(r'\d.+?\n')
output_list = reg_2.findall(final_output)

final_output_list = []
for i in output_list:
   final_output_list.append(i.strip())
   
#create a dictionary of all the results from abpackingangle
output_dict = {}
for b in final_output_list:
   i = b.split(': ')
   output_dict[i[0]] = i[1]

#write dictionary into csv file
with open ('packingAngleOutput.csv', 'w') as f:
   w = csv.writer(f)
   w.writerows(output_dict.items())

