import sys

class Func:
  "store a function info"
  def __init__(self, str, parent = None):
    self.parent = parent
    self.children = ()
    
    segs = str.split()
    self.time = float(segs[0])
    self.cpu = int(segs[2][0:-1])
    self.proc = segs[3]
    if segs[-3] == 'us':
      self.duration = float(segs[-4])
      self.name = segs[-1].rstrip(';')
    else:
      self.duration = 0
      self.name = segs[-2]

# Main
file = sys.argv[-1]
trace = open(file, 'r')

for i in range(5):
  trace.readline()

  
