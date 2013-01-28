import sys
from collections import defaultdict

import traceparser as parser

# Main

file = sys.argv[-1]
parser.parse_file(file)

# Prints the function sequence
for func in parser.func_list:
  print func.to_string()

print "Number of skipped lines: %d" % parser.num_skipped
print "Number of partial function exits: %d" % parser.num_partial_exit

# Prints the highest level functions
for proc in parser.proc_dict.keys():
  root = parser.proc_dict[proc]
  func_stat = defaultdict(list)
  for func in root.children:
    func_stat[func.name].append(func.duration)
  print "%s\n%s" % (proc, func_stat)
  
  for func in root.broken_entries:
    print "Broken Entry: %s" % func.to_string()