set arrow from 1,1.11 to 117,1.11 nohead lt 4 lw 10
set arrow from 118,1.09 to 140,1.09 nohead lt 1 lw 40
set arrow from 141,1.07 to 152,1.07 nohead lt 3 lw 10
set arrow from 153,1.09 to 175,1.09 nohead lt 1 lw 40
set arrow from 176,1.11 to 201,1.11 nohead lt 4 lw 10
set arrow from 202,1.09 to 224,1.09 nohead lt 1 lw 40
set arrow from 225,1.07 to 236,1.07 nohead lt 3 lw 10
set arrow from 237,1.09 to 259,1.09 nohead lt 1 lw 40
set arrow from 260,1.11 to 284,1.11 nohead lt 4 lw 10
set arrow from 285,1.09 to 307,1.09 nohead lt 1 lw 40
set arrow from 308,1.07 to 331,1.07 nohead lt 3 lw 10
set arrow from 332,1.09 to 354,1.09 nohead lt 1 lw 40
set arrow from 355,1.11 to 368,1.11 nohead lt 4 lw 10
set arrow from 369,1.09 to 391,1.09 nohead lt 1 lw 40
set arrow from 392,1.07 to 408,1.07 nohead lt 3 lw 10
set key below
set title "TMHMM posterior probabilities for 4n6h_A"
set yrange [0:1.2]
set size 2., 1.4
#set xlabel "position"
set ylabel "probability"
set xrange [1:408]
# Make the ps plot
set term postscript eps color solid "Helvetica" 30
set output "./TMHMM_1/4n6h_A.eps"
plot "./TMHMM_1/4n6h_A.plp" using 1:4 title "transmembrane" with impulses lt 1 lw 2, \
"" using 1:3 title "inside" with line lt 3 lw 2, \
"" using 1:5 title "outside" with line lt 4 lw 2
exit
