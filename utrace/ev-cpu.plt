set terminal postscript eps color
set output 'ev-cpu.eps'
set size 3,0.5

set ylabel 'CPU Usage (%)'
set yrange [0:100]
set y2label 'Staleness (KB)'
set xlabel 'Time (s)'

plot '.cpu-data.txt' using 1:2 title 'CPU' axes x1y1 with lines lt 1 lw 0.2, \
  '.kern-data.txt' using 1:2 title 'Staleness' axes x1y2 with lines lt 4 lw 2, \
  '.ev-data.txt' using 1:2 title 'Touches' axes x1y1 with points
