
################################################################################
#	DOCKERFILE
#	MemSatSVM - CPU based
#
#	Repo: https://github.com/psipred/MemSatSVM.git
#
#	Nugent, T. & Jones, D.T. (2009) Transmembrane protein topology prediction 
#	using support vector machines. BMC Bioinformatics. 10, 159. Epub
# 
################################################################################

# Start from 
FROM ubuntu:18.04

# Install packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils \
		git build-essential \ 
		wget bash ncbi-blast+ pkg-config libgd-dev

ENV HOME=/home/
ENV MakeNoOfThreads=12


# Install legacy blast 
WORKDIR /home/
RUN wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/legacy.NOTSUPPORTED/2.2.26/blast-2.2.26-x64-linux.tar.gz
RUN tar -xvzf blast-2.2.26-x64-linux.tar.gz
RUN rm blast-2.2.26-x64-linux.tar.gz

# Clone & Download
WORKDIR /home/
RUN git clone https://github.com/psipred/MemSatSVM.git

WORKDIR /home/MemSatSVM/
RUN wget http://bioinfadmin.cs.ucl.ac.uk/downloads/memsat-svm/models.tar.gz
RUN tar -zxvf models.tar.gz

# Build & Install

# deal with hardcoded paths
RUN sed -i 's|CFLAGS=-O3|CFLAGS=-fno-pie -no-pie -O3|g' Makefile	
RUN sed -i 's|LFLAGS=-O3|LFLAGS=-fno-pie -no-pie -O3|g' Makefile	

RUN make -j $MakeNoOfThreads
RUN cpan -i GD

RUN sed -i "s|my \$mem_dir = '';|my \$mem_dir = '/home/MemSatSVM/';|g" run_memsat-svm.pl		
RUN sed -i "s|my \$ncbidir = '';|my \$ncbidir = '/home/blast-2.2.26/bin/';|g" run_memsat-svm.pl		
RUN sed -i "s|my \$dbname = '';|my \$dbname = '/home/database/\$ENV\${protDB}';|g" run_memsat-svm.pl


# Create folders for input and output data
RUN mkdir /input
RUN mkdir /output
ENV PATH=${PATH}:/home/MemSatSVM/


################################################################################
