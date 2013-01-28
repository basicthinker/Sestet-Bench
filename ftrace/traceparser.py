import sys
from collections import defaultdict

class Func:
  def __init__(self, line = None):
    self.children = []
    
    if line is None: # happens in default dict
      self.__parent = self # indicates an abstract root node
      self.name = 'root'
      self.proc = None # set after initialization
      self.cur_parent = self
      self.depth = 0
      self.broken_entries = []
      return

    self.__parent = None
    segs = line.split('|')
    self.time = float(segs[0])
  
    cpu_proc = segs[1].split(')')
    self.cpu = int(cpu_proc[0])
    self.proc = cpu_proc[1].strip()
    if self.proc == '<idle>-0': # as every processor has an idle process
      self.proc = str(self.cpu) + self.proc
    
    time_unit = segs[2].split()
    if len(time_unit) > 0: # containing time
      if time_unit[1] == 'us':
        self.duration = float(time_unit[0])
      elif time_unit[1] == 'ms':
        self.duration = float(time_unit[0]) * 1000
      else:
        sys.stderr.write("[Error] Func.__init__ meets invalid time unit: %s\n" \
                         % time_unit[1]);
        sys.exit(-1)
      
      if segs[-1].rstrip()[-1] == '}' or segs[-1].rstrip()[-1] == '/':
        self.name = None # indicates a closing bracket
        self.entry_name = None
        if segs[-1].rstrip()[-1] == '/':
          self.entry_name = segs[-1].strip('} /*\n')
      else:
        self.name = segs[-1].strip('() ;\n')
    elif segs[-1].rstrip()[-1] == '{': # containing an opening bracket
      self.duration = 0
      self.name = segs[-1].strip('() {\n')
    else:
      sys.stderr.write("[Error] Func.__init__() meets invalid line: %s\n" \
                       % line)
      sys.exit(-1)
        
    i = 0
    while segs[-1][i] == ' ':
      i += 1
    self.depth = i / 2
    return

  def is_root(self):
    return self.__parent == self
      
  def get_parent(self):
    return self.__parent

  def set_parent(self, parent):
    if self.__parent is None:
      self.__parent = parent
      parent.children.append(self)
    else:
      sys.stderr.write("[Error] Func.set_parent() duplicated: %s\n" % self.name)
      sys.exit(-1)

  def to_string(self):
    if self.is_root():
      return "root of %s" % self.proc
    else:
      return "Func: name=%s, parent=%s, time=%f, cpu=%d, proc=%s, " \
          "duration=%f depth=%d" \
          % (self.name, self.__parent.name, \
             self.time, self.cpu, self.proc, self.duration, self.depth)
# Func

proc_dict = defaultdict(Func) # contains trees of functions
func_list = [] # contains functions in time order

def find_root(func):
  root = proc_dict[func.proc]
  root.proc = func.proc # in case the first access to defaultdict
  return root

def cur_parent(func):
  root = find_root(func)
  return root.cur_parent

num_partial_exit = 0
# Return new parent for the next line
def do_process(parent, line):
  global num_partial_exit

  func = Func(line)

  # change parent if necessary
  if parent is None: # only happens in first call
    parent = find_root(func)
  elif func.proc != parent.proc: # happens when switching context
    find_root(parent).cur_parent = parent
    parent = cur_parent(func)
  
  broken_entries = find_root(func).broken_entries
  if func.name is None: # closing bracket
    if func.entry_name:
      # first check former unmatched function entries
      for entry in broken_entries:
        if func.entry_name == entry.name and func.depth == entry.depth:
          entry.duration = func.duration
          broken_entries.remove(entry)
          return parent # as if this line is not meet
      
      while not parent.is_root() and parent.name != func.entry_name:
        broken_entries.append(parent)
        parent = parent.get_parent()
      parent.duration = func.duration
      return parent.get_parent()
    else:
      if func.depth > parent.depth: # partial exit
        num_partial_exit += 1
        return parent
      else:
        while parent.depth > func.depth: # possible partial entry
          broken_entries.append(parent)
          parent = parent.get_parent()
        parent.duration = func.duration
        return parent.get_parent()
  else:
    while parent.depth > func.depth - 1:
      broken_entries.append(parent)
      parent = parent.get_parent()
    func.set_parent(parent)
    func_list.append(func)
    if line.rstrip()[-1] == '{': # opening bracket
      return func
    elif line.rstrip()[-1] == ';': # whole function
      return parent
    else:
      sys.stderr.write("[Error] do_process: %s\n" % line)
      sys.exit(-1)

num_skipped = 0
def skip_partial(trace):
  global num_skipped
  while True:
    line = trace.readline()
    segs = line.split('|')
    if len(segs[-1]) < 3:
      continue
    elif segs[-1][2] == ' ' or \
        segs[-1].rstrip()[-1] == '}' or segs[-1].rstrip()[-1] == '/':
      num_skipped += 1
      continue
    else:
      break
  return line

def parse_file(file):
  trace = open(file, 'r')

  # skips partial trace
  line = skip_partial(trace)
  if not line:
    print "No valid lines."
    sys.exit(0)

  parent = do_process(None, line)

  line = trace.readline()

  line_count = 0
  while line:
    if len(line) > 2:
      if line.rstrip()[-1] == ']':
        print line.rstrip()
        line = skip_partial(trace)
        continue
      elif line.rstrip()[-1] == '-':
        trace.readline() # skips context switch info
        trace.readline()
      elif line.rstrip()[-1] != '|':
        parent = do_process(parent, line)
    line = trace.readline()
    line_count += 1
    if line_count % 50000 == 0:
      sys.stderr.write("... Finishing %d lines ...\n" % line_count)

