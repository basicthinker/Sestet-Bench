import sys

if len(sys.argv) != 2:
  print "Usage: %s FilterList" % sys.argv[0]
  sys.exit(-1)

file = open(sys.argv[1], 'r')

print "#! /system/bin/sh"
print 
print "echo function_graph > /d/tracing/current_tracer"
print "echo funcgraph-cpu > /d/tracing/trace_options"
print "echo funcgraph-proc > /d/tracing/trace_options"
print "echo funcgraph-abstime > /d/tracing/trace_options"
print "echo nofuncgraph-overhead > /d/tracing/trace_options"

print
print "umount tmp 2>/dev/null"
print "mount -o rw,remount /"
print "mkdir /tmp"
print "mount -t ramfs none /tmp"
print "echo 0 > /d/tracing/tracing_enabled"

print
for line in file:
  line = line.strip()
  print "echo '%s' >> /d/tracing/set_ftrace_filter" % line
  print "cat /d/tracing/set_ftrace_filter | busybox grep -c '%s'" % line
  print
  
