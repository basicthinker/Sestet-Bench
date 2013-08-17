set terminal png
set output 'opt-ratio.png'
set ylabel 'Opt Ratio (%)'
set yrange [0:100]
set xlabel 'Staleness (KB)'

plot '.kern-data.txt' using 2:5 title '' with lines
