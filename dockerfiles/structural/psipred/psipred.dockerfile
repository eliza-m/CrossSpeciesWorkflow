
################################################################################
#	DOCKERFILE
#	Psipred v4.0 using BLAST+
#
#	GitHub Repos: 
#	https://github.com/psipred/psipred
#
#	References:
#
#	Buchan DWA, Jones DT (2019). The PSIPRED Protein Analysis Workbench: 
#	20 years on. Nucleic Acids Research. https://doi.org/10.1093/nar/gkz297
#
#	Jones DT. (1999) Protein secondary structure prediction based on 
#	position-specific scoring matrices. J. Mol. Biol. 292: 195-202.
#
#	Hanson, J., Paliwal, K., Litfin, T., Yang, Y., & Zhou, Y. (2019). 
#	Improving prediction of protein secondary structure, backbone angles, 
#	solvent accessibility and contact numbers by using predicted contact 
#	maps and an ensemble of recurrent and residual convolutional neural 
#	networks. Bioinformatics (Oxford, England), 35(14), 2403–2410. 
#	https://doi.org/10.1093/bioinformatics/bty1006	
#
################################################################################


# TODO 
# inspect compiling warnings
# do something with the hardcoded paths especially for uniref90
# make legacy blast work properly ... pfilt and formatdb
# https://www.biostars.org/p/70342/
# find out how "experimental" the hhblits support is and wether it can be integrated


# Start from 
FROM ubuntu:18.04

# Install packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils \
		git build-essential cmake \ 
		wget bash tcsh ncbi-blast+

# Set environment variables
ENV DBname=uniref50.fasta
ENV DBfolder=/home/database/
ENV MakeNoOfThreads=4
ENV CPUnum=10

# Install some dependacies 
WORKDIR /home/
RUN wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/legacy.NOTSUPPORTED/2.2.26/blast-2.2.26-x64-linux.tar.gz
RUN tar -xvzf blast-2.2.26-x64-linux.tar.gz
RUN rm blast-2.2.26-x64-linux.tar.gz


##############################
#	Psipred
##############################

# Clone & Build the Psipred
WORKDIR /home/
RUN git clone --recursive https://github.com/psipred/psipred.git
RUN mkdir database

WORKDIR /home/psipred/src/
RUN make -j $MakeNoOfThreads
RUN make install


# setting up the hardcoded paths
# in legacy blast
WORKDIR /home/psipred/
RUN sed -i 's|set dbname = /scratch1/NOT_BACKED_UP/dbuchan/uniref/uniref90.fasta|set dbname = ${DBfolder}/${DBname}|g' runpsipred		
RUN sed -i 's|set ncbidir = /scratch0/NOT_BACKED_UP/dbuchan/Applications/blast-2.2.26/bin|set ncbidir = /home/blast-2.2.26/bin|g' runpsipred		

# for blast+ 
WORKDIR /home/psipred/BLAST+/

# deal with hardcoded paths
RUN sed -i 's|set dbname = /scratch1/NOT_BACKED_UP/dbuchan/uniref/uniref90.fasta|set dbname = ${DBfolder}/${DBname}|g' runpsipredplus		
RUN sed -i 's|set ncbidir = /scratch0/NOT_BACKED_UP/dbuchan/Applications/ncbi-blast-2.2.31+/bin/|set ncbidir = /usr/bin/|g' runpsipredplus		
RUN sed -i 's|set datadir = ../data|set datadir = /home/psipred/data|g' runpsipredplus		
RUN sed -i 's|set execdir = ../bin|set execdir = /home/psipred/bin|g' runpsipredplus	

# make possible the usage of multiple CPU threads
RUN sed -i 's|-num_alignments 0|-num_alignments 0 -num_threads ${CPUnum}|g' runpsipredplus	


# Create folders for input and output data
RUN mkdir /input
RUN mkdir /output


# Setting working directory when docker image is running
# messy workaround...to hijack all the relative paths issues...
ENV psipredplus="/home/psipred/BLAST+/runpsipredplus"


################################################################################

