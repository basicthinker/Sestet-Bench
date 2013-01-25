import sys

class Func:
  "store a function info"
  def __init__(self, parent, str):
    self.parent = parent
    self.children = ()
    
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

proc_list = [] # contains trees of functions
func_list = () # contains functions in time order

# Return new parent for the next line
def do_process(parent, line):
  if line[-1] == '}' or line[-1] == '/':
    segs = line.split()
    parent.duration = float(segs[5])
    return parent.parent
 
  func = Func(parent, line)
  func_list.append(func)
  
  if parent is None: # root node
    proc_list[func.proc].append(func)
  else:
    parent.children.append(func)
  
  if line[-1] == '{':
    return func
  elif line[-1] == ';':
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
  print line
  segs = line.split('|')
  if segs[-1][2] == ' ' or segs[-1][-1] != '{':
    continue
  else:
    break

parent = do_process(None, line)

for line in trace:
  if line[-1] == '|':
    continue
  parent = do_process(parent, line)
