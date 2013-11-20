#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 TraceDataDirectory"
  exit 1
fi

trace_dir=$1
for trace_file in `ls $trace_dir/*-io-*.trace`
do
  ./simu-io-trace.out $trace_file 5 .io-plt.data .stal-ev-plt.data
  gnuplot opt-ratio.plt
  mv opt-ratio.eps ${trace_file/\.trace/\.eps}
  if [ $? = 0 ]; then
    rm .io-plt.data .stal-ev-plt.data
  fi
done

