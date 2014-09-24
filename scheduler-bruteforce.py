#!/usr/bin/env python
# 
# Interview Scheduler
# Creates all possible schedules and outputs combinations with the least conflicts
# Attempts to keep the day before interview free as well
# 
# Input file should be of format:
#    Program1 - Sat 12/6/14, Sat 12/13/14
#    Program2 - Fri 12/12/14, Sat 1/10/15
# 
# Vivek Sant
# 2014-09-23
# 

import itertools
import datetime, time

FILE = "programs-dates.txt"

def num_conflicts(combo):
  return len(combo) - len(list(set(combo)))

def num_conflicts_preday(combo):
  newarr = []
  for i in combo:
    newarr.append(i)
    newarr.append(i - datetime.timedelta(days=1))
  return len(newarr) - len(list(set(newarr)))

# Read in the data file of programs and possible dates
data = open(FILE).read().strip().split('\n')
programs = []
program_dates = []
program_dates_dict = {}
for row in data:
  prog, datearr = row.split(' - ')
  programs.append(prog)
  program_dates.append([datetime.datetime(*(time.strptime(x, '%a %m/%d/%y')[0:6])) for x in datearr.split(', ')])

# Create all combos and assess number of conflicts
combos = list(itertools.product(*program_dates))
for combo in combos:
  num = num_conflicts_preday(combo)
  if num not in program_dates_dict.keys():
    program_dates_dict[num] = [combo]
  else:
    program_dates_dict[num].append(combo)

lowest_conflicts = sorted(program_dates_dict.keys())[0]
print str(len(combos)) + " possibilities, " + "lowest # conflicts = " + str(lowest_conflicts) + ", " + str(len(program_dates_dict[lowest_conflicts])) + " options"
for i in program_dates_dict[lowest_conflicts]:
  for idx, val in enumerate(programs):
    print val + ": " + i[idx].strftime('%a %m/%d/%y')
  print