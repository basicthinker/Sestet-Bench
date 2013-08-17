import sys
import string

if len(sys.argv) != 3:
  print "Usage: python %s KernTraceFile EventTraceFile" % sys.argv[0]
  sys.exit(1)

kern_file = open(sys.argv[1], 'r')
ev_file = open(sys.argv[2], 'r')

line = kern_file.readline()
while line.find("begin time") < 0:
  line = kern_file.readline()
begin_time = float(line[line.index('[') + 1:line.index(']')])

for line in ev_file:
  segs = string.split(line, '\t')
  print "%.3f\t50" % (float(segs[1]) - begin_time)

kern_file.close()
ev_file.close()
