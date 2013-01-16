import sys
import string

INTERVAL = 0.0002

def fetch_on(fp, start, end):
  sum = 0
  while True:
    line = fp.readline()
    if not line:
      break
    segments = string.split(line, ',')
    time = float(segments[0])
    if time < start:
      continue
    if time >= end:
      break
    mA = float(segments[1])
    V = float(segments[2])
    sum += mA * V;
  
  sum *= INTERVAL
  return sum

# Main
if len(sys.argv) != 3:
  print "Usage: python %s LogFile IntervalFile" % sys.argv[0]
  sys.exit(-1)

log = sys.argv[1]
intervals = sys.argv[2]

log_file = open(log, 'r')
int_file = open(intervals, 'r')

line = log_file.readline() # skips the field names
for line in int_file:
  segments = string.split(line, '\t')
  start = float(segments[0])
  end = float(segments[1])
  print fetch_on(log_file, start, end)

