# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

HOST = 'localhost'
PORT = 3306
USER = 'root'
DB = 'sestet'

# Main

if len(sys.argv) != 4:
  print "Usage: %s TrialName TraceFile ProcessFile" % sys.argv[0]
  exit(-1)

trial_spec = sys.argv[1]
trace_file = open(sys.argv[2], 'r')
process_file = open(sys.argv[3], 'r')

conn = None

try:
  conn = mdb.connect(host = HOST, user = USER, port = PORT, db = DB)
  cursor = conn.cursor()
  cursor.execute("SELECT add_trial('%s')" % trial_spec)
  trial_id = cursor.fetchone()[0]
  print trial_id
  
  cursor.callproc('add_process', ('test4', 'test', 5))

except mdb.Error, e:
  sys.stderr.write("[Error %d] %s\n" % (e.args[0], e.args[1]))

finally:
  if conn:
    conn.close()