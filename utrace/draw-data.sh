#!/bin/bash

LOG_POST=".log"

if [ $# -ne 1 ]; then
  echo "Usage: $0 TraceDataDirectory"
  exit 1
fi

trace_dir=$1
kern_data_files=`ls $trace_dir/*-kern-*.log`
for kern_file in $kern_data_files
do
  ev_file=${kern_file/'-kern-'/'-ev-'}
  cpu_file=${kern_file/'-kern-'/'-cpu-'}
  python proc-kern-data.py $kern_file > .kern-data.txt
  python proc-cpu-data.py $cpu_file > .cpu-data.txt
  python proc-ev-data.py $kern_file $ev_file > .ev-data.txt
  gnuplot opt-ratio.plt
  gnuplot ev-cpu.plt
  mv opt-ratio.png ${kern_file%$LOG_POST}'-opt-ratio.png'
  mv ev-cpu.eps ${kern_file%$LOG_POST}'-ev-cpu.eps'
  if [ $? = 0 ]; then
    rm .kern-data.txt .cpu-data.txt .ev-data.txt
  fi
done

