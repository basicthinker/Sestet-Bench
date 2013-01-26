import sys
from collections import defaultdict

class Func:
  def __init__(self, line = None):
    self.children = []
    
    if line is None:
      self.__parent = None
      self.name = 'root'
      self.proc = None
      self.cur_parent = self
      return

    segs = line.split()
    self.time = float(segs[0])
    self.cpu = int(segs[2][0:-1])
    self.proc = segs[3]
    
    if self.proc == '<idle>-0':
      self.proc = str(self.cpu) + self.proc
    
    if segs[-3] == 'us':
      self.duration = float(segs[5])
      if line[-2] == '}' or line[-2] == '/':
        self.name = None
      else:
        self.name = segs[-1].rstrip(';')
    else:
      self.duration = 0
      self.name = segs[-2]
    return

  def is_root(self):
    return self.__parent is None
      
  def get_parent(self):
    return self.__parent

  def set_parent(self, parent):
    self.__parent = parent
    parent.children.append(self)
      
  def to_string(self):
    if self.is_root():
      return "root of %s" % self.proc
    else:
      return "Func: name=%s, parent=%s, time=%f, cpu=%d, proc=%s, duration=%f" \
          % (self.name, self.__parent.name, \
             self.time, self.cpu, self.proc, self.duration)

proc_dict = defaultdict(Func) # contains trees of functions
func_list = [] # contains functions in time order

# Return new parent for the next line
def do_process(parent, line):
 
  func = Func(line)

  if parent is None:
    parent = proc_dict[func.proc]
    parent.proc = func.proc
  elif func.proc != parent.proc:
    proc_dict[parent.proc].cur_parent = parent
    root = proc_dict[func.proc]
    parent = root.cur_parent
    root.proc = func.proc # in case the first access

  if func.name is None:
    parent.duration = func.duration
    return parent.get_parent()
  else:
    func.set_parent(parent)
    if line[-2] == '{':
      return func
    elif line[-2] == ';':
      return func.get_parent()
    else:
      print "[Error] do_process: %s" % line
      sys.exit(-1)

def skip_partial(trace):
  while True:
    line = trace.readline()
    segs = line.split('|')
    if segs[-1][2] == ' ' or segs[-1][-2] == '}' or segs[-1][-2] == '/':
      continue
    else:
      break
  return line

# Main

file = sys.argv[-1]
trace = open(file, 'r')

# skips partial trace
line = skip_partial(trace)

parent = do_process(None, line)

line = trace.readline()
while line:
  if len(line) > 2:
    if line[-2] == ']':
      print line
      line = skip_partial(trace)
      continue
    elif line[-2] == '-':
      trace.readline() # skips context switch info
      trace.readline()
    elif line[-2] != '|':
      parent = do_process(parent, line)
  line = trace.readline()

# Prints the highest level functions
for proc in proc_dict.keys():
  root = proc_dict[proc]
  func_set = set()
  for func in root.children:
    func_set.add(func.name)
  print "%s\n%s" % (proc, func_set)
