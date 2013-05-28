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
    mW = float(segments[1])
    sum += mW;
  
  sum *= INTERVAL
  return sum

# Main
if len(sys.argv) != 4:
  print "Usage: python %s LogFile IntervalFile OutputColumnNum" % sys.argv[0]
  sys.exit(-1)

log = sys.argv[1]
intervals = sys.argv[2]
columns = int(sys.argv[3])

log_file = open(log, 'r')
int_file = open(intervals, 'r')

line = log_file.readline() # skips the field names
index = 0;
for line in int_file:
  segments = string.split(line, '\t')
  start = float(segments[0])
  end = float(segments[1])
  index += 1
  if index % columns == 0:
    print fetch_on(log_file, start, end)
  else:
    print "%f\t" % fetch_on(log_file, start, end),
