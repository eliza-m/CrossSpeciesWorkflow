set arrow from 1,1.07 to 12,1.07 nohead lt 3 lw 10
set arrow from 13,1.09 to 35,1.09 nohead lt 1 lw 40
set arrow from 36,1.11 to 44,1.11 nohead lt 4 lw 10
set arrow from 45,1.09 to 67,1.09 nohead lt 1 lw 40
set arrow from 68,1.07 to 118,1.07 nohead lt 3 lw 10
set arrow from 119,1.09 to 141,1.09 nohead lt 1 lw 40
set arrow from 142,1.11 to 145,1.11 nohead lt 4 lw 10
set arrow from 146,1.09 to 165,1.09 nohead lt 1 lw 40
set arrow from 166,1.07 to 245,1.07 nohead lt 3 lw 10
set arrow from 246,1.09 to 268,1.09 nohead lt 1 lw 40
set arrow from 269,1.11 to 540,1.11 nohead lt 4 lw 10
set key below
set title "TMHMM posterior probabilities for 5l22_B"
set yrange [0:1.2]
set size 2., 1.4
#set xlabel "position"
set ylabel "probability"
set xrange [1:540]
# Make the ps plot
set term postscript eps color solid "Helvetica" 30
set output "./TMHMM_1/5l22_B.eps"
plot "./TMHMM_1/5l22_B.plp" using 1:4 title "transmembrane" with impulses lt 1 lw 2, \
"" using 1:3 title "inside" with line lt 3 lw 2, \
"" using 1:5 title "outside" with line lt 4 lw 2
exit
