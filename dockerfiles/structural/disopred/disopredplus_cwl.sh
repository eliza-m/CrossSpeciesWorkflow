
cd $HOME

cp $1 .
fasta="$(basename -- $1)"

/home/disopred/BLAST+/run_disopred_plus.pl $fasta