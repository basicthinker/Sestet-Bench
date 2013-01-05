import sys
import string

INTERVAL = 0.0002

if len(sys.argv) != 4:
    print "Usage: python %s FileName StartTime EndTime" % sys.argv[0]
    sys.exit(-1)

file = sys.argv[1]
startTime = float(sys.argv[2])
endTime = float(sys.argv[3])

fp = open(file, 'r')
fp.readline() # skips the field names

uAs = 0
for line in fp:
    segments = string.split(line, ',')
    time = float(segments[0])
    if time < startTime:
        continue
    if time >= endTime:
        break
    mW = float(segments[1])
    V = float(segments[2])
    uAs += mW / V * 1000 * INTERVAL

uAh = uAs / 3600
print "Sum of Energy (uAh): \t%f" % uAh