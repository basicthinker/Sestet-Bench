set terminal postscript eps color
set output 'opt-ratio.eps'
set ylabel 'Opt Ratio (%)'
set yrange [0:100]
set xlabel 'Staleness (KB)'

plot '.io-plt.data' using 1:2 title 'Ext4' with lines, \
  '' using 1:3 title 'AdaFS' with lines, \
  '.stal-ev-plt.data' using 1:2 title 'fsync' with impulses 
