#!/usr/bin/env python

# Sam Addis 31/05/19
# V1.2
# Code seperating the target PDB codes with multiple entries from the single
# entry PDB codes for antibodies in the Redundant PDB code list from
# bioinf.org.uk/abs/abdb

import re
NR = ''
R = ''
with open('redundant_antibody_list.txt') as f:
          for line in f.read().split('\n'):
              if re.search(r',', line):
                  R += line + '\n'
              else:
                  NR += line + '\n'

non_redundant_txt = open('non_redundant_ab.txt', 'w+')
non_redundant_txt.write(NR)
non_redundant_txt.close()

redundant_txt = open('redundant_ab.txt', 'w+')
redundant_txt.write(R)
redundant_txt.close()

          
                  
                  
            
