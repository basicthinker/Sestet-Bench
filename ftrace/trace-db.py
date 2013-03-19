# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import traceparser as parser

HOST = 'localhost'
PORT = 3306
USER = 'root'
DB = 'sestet'

# Main

if len(sys.argv) != 3:
  print "Usage: %s TrialName TraceFile" % sys.argv[0]
  exit(-1)

trial_spec = sys.argv[1]

parser.parse_file(sys.argv[2])

conn = None
cursor = None


try:
  conn = mdb.connect(host = HOST, user = USER, port = PORT, db = DB)
  cursor = conn.cursor()
  cursor.execute("SELECT add_trial('%s')" % trial_spec)
  trial_id = cursor.fetchone()[0]
  print "Trial#: %d" % trial_id
  
  for func in parser.func_list:
    cursor.callproc('add_function', \
                    (func.name, func.get_parent().name, \
                     func.time, func.cpu, func.pid, func.proc, \
                     func.duration, func.depth, trial_id))
  conn.commit()

  print "Number of skipped lines: %d" % parser.num_skipped
  print "Number of partial function exits: %d" % parser.num_partial_exit
  for proc in parser.proc_dict.keys():
    print "Broken entry number of %s: %d" % \
        (proc, len(parser.proc_dict[proc].broken_entries))

except mdb.Error, e:
  sys.stderr.write("[Error %d] Main: %s\n" % (e.args[0], e.args[1]))

finally:
  conn.commit()
  if cursor:
    cursor.close()
  if conn:
    conn.close()