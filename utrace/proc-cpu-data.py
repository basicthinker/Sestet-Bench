import sys
import string

if len(sys.argv) != 2:
  print "Usage: python %s CPUTraceFile" % sys.argv[0]
  sys.exit(1)

cpu_file = open(sys.argv[1], 'r')

begin_time = float(cpu_file.readline())

for line in cpu_file:
  segs=string.split(line, '\t')
  print "%.3f\t%s" % (float(segs[0]) - begin_time, segs[1])

cpu_file.close()
