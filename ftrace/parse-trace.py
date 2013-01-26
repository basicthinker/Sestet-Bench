import sys
from collections import defaultdict

class Func:
  "store a function info"
  def __init__(self, parent, str):
    self.parent = parent
    self.children = []
    
    segs = str.split()
    self.time = float(segs[0])
    self.cpu = int(segs[2][0:-1])
    self.proc = segs[3]
    if segs[-3] == 'us':
      self.duration = float(segs[5])
      self.name = segs[-1].rstrip(';')
    else:
      self.duration = 0
      self.name = segs[-2]
    return

  def Print(self):
    if self.parent is None:
      parent = "root"
    else:
      parent = self.parent.name

    print "Func: name=%s, parent=%s, time=%f, cpu=%d, proc=%s, duration=%f" \
        % (self.name, parent, self.time, self.cpu, self.proc, self.duration)
    return

proc_list = defaultdict(list) # contains trees of functions
func_list = [] # contains functions in time order

# Return new parent for the next line
def do_process(parent, line):
  if line[-2] == '}' or line[-2] == '/':
    segs = line.split()
    parent.duration = float(segs[5])
    return parent.parent
 
  func = Func(parent, line)
  func_list.append(func)
  
  if parent is None: # root node
    proc_list[func.proc].append(func)
  else:
    parent.children.append(func)
  
  if line[-2] == '{':
    return func
  elif line[-2] == ';':
    return parent
  else:
    print "[Error] do_process: %s" % line
    sys.exit(-1)


# Main

file = sys.argv[-1]
trace = open(file, 'r')

for i in range(5):
  trace.readline()

# skips partial trace
while True:
  line = trace.readline()
  segs = line.split('|')
  if segs[-1][2] == ' ' or segs[-1][-2] == '}' or segs[-1][-2] == '/':
    continue
  else:
    break

parent = do_process(None, line)

for line in trace:
  if len(line) < 2 or line[-2] == '|':
    continue
  parent = do_process(parent, line)

for func in func_list:
  func.Print()
