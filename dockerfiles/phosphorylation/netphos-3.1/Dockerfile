
################################################################################
#	DOCKERFILE
#		
#	NetPhos v3.1 :
#
#	Priorly running this dockerfile, it is required to access the above link
#	and consult the license agreement terms. If you are eligible to use
#	and download the software (indicated bellow) please register to DTU 
#	Health Tech and download and then copy inside the current directory
#	the following software :
#
#	Link : https://services.healthtech.dtu.dk/software.php
#
#
#	References: 
#
#	Blom, N., Gammeltoft, S., and Brunak, S. Sequence- and structure-based 
#	prediction of eukaryotic protein phosphorylation sites. Journal of 
#	Molecular Biology: 294(5): 1351-1362, 1999. 
#	
#	Blom N, Sicheritz-Ponten T, Gupta R, Gammeltoft S, Brunak S. Prediction 
#	of post-translational glycosylation and phosphorylation of proteins 
#	from the amino acid sequence. Proteomics: Jun;4(6):1633-49, review 2004.
#
################################################################################

# Start from 
FROM ubuntu:18.04

# Install packages
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils \
		git build-essential \ 
		tcsh bash gnuplot netpbm \
		gawk python2.7


# Install NetPhos v3.1 

RUN mkdir /home/netphos-3.1
COPY ./netphos-3.1* /home/netphos-3.1/

WORKDIR /home/netphos-3.1/
RUN zcat *.Z | tar -xvf -

WORKDIR ape-1.0/
RUN mkdir -p /scratch

# deal with some hard coded paths
RUN sed -i 's|/usr/cbs/bio/src/ape-1.0|/home/netphos-3.1/ape-1.0|g' ape 		
RUN sed -i 's|setenv PYTHON /usr/local/python/bin/python|setenv PYTHON /usr/bin/python2.7|g' ape 		
RUN sed -i 's|setenv  MAXCPU  5|/setenv  MAXCPU  $ENV{MAXCPU}|g' ape 		

# because there is no option for x86_64. Binaries are available only for i386 and ia64...
RUN sed -i "s|\`uname -m\`|i386|g" ape ;


# Create folders for input and output data
RUN mkdir -p /input
RUN mkdir -p /output

# Setting working directory when docker image is running
WORKDIR /home/

