
################################################################################
#	DOCKERFILE
#	
#	TMHMM v2.0 
#
#	Reference (vor v1): 
#
#	Krogh A, Larsson B, von Heijne G, Sonnhammer EL. Predicting transmembrane
# 	protein topology with a hidden Markov model: application to complete 
#	genomes. J Mol Biol. 2001;305(3):567-580. doi:10.1006/jmbi.2000.4315
#
#	
#	Priorly running this dockerfile, it is required to access the above link
#	and consult the license agreement terms. If you are eligible to use
#	and download the software (indicated bellow) please register to DTU 
#	Health Tech and download and then copy inside the current directory
#	the following software :
#
#	Download link : https://services.healthtech.dtu.dk/software.php
#
################################################################################

# Start from 
FROM ubuntu:18.04


# Install packages
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils \
		build-essential \ 
		bash gnuplot
		
WORKDIR /home/
COPY ./tmhmm-2.0c* /home/
RUN tar -xvf tmhmm-2.0c.Linux.tar.gz

WORKDIR /home/tmhmm-2.0c/
ENV PATH "$PATH:/home/tmhmm-2.0c/bin/"
RUN sed -i "s|/usr/local/bin/|/usr/bin/|g" bin/*

# Create folders for input and output data
RUN mkdir -p /input
RUN mkdir -p /output

