#! /bin/bash
if [ $# != 3 ]; then
  echo "Usage: $0 TraceFile Keyword"
fi

file=$1
keyword=$2

cat $file | grep "$keyword" | awk '
  BEGIN{
    num_lines=0;
    time=0;
  }
  {
    num_lines+=1;
    time+=$6;
    print $0;
  }
  END{
    print "\nAll:"
    print "\tNumber of lines: " num_lines
    print "\tTotal func time: " time " us"
    print "---"
  }
'

cat $file | grep "/\*.*$keyword.*\*/" | awk '
  BEGIN{
    num_lines=0;
    time=0;
  }
  {
    if ($6 > 1000) {
      num_lines+=1;
      time+=$6;
      print $0;
    }
  }
  END{
    print "\nLong calls (> 1 ms):"
    print "\tNumber of long-call lines: " num_lines
    print "\tTotal time of long calls: " time/1000 " ms"
    print "------"
  }
'
