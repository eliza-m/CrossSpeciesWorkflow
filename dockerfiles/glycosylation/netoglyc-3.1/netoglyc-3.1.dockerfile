
################################################################################
#	DOCKERFILE
#		
#	NetOglyc v3.1 :
#
#	Priorly running this dockerfile, it is required to access the above link
#	and consult the license agreement terms. If you are eligible to use
#	and download the software (indicated bellow) please register to DTU 
#	Health Tech and download and then copy inside the current directory
#	the following software :
#
#	Link : https://services.healthtech.dtu.dk/software.php
#
#	Additionally, NetOglyc uses SignalP software from DTU that needs to be 
#	downloaded from the above link and copied to the current directory.
#
#	Reference: 
#	Steentoft C, Vakhrushev SY, Joshi HJ, Kong Y, Vester-Christensen MB, 
#	Schjoldager KT, Lavrsen K, Dabelsteen S, Pedersen NB, Marcos-Silva L, 
#	Gupta R, Bennett EP, Mandel U, Brunak S, Wandall HH, Levery SB, Clausen 
#	H. Precision mapping of the human O-GalNAc glycoproteome through 
#	SimpleCell technology. EMBO J, 32(10):1478-88, 2013.
#
################################################################################

# Start from 
FROM ubuntu:18.04

# Install packages
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils build-essential bash tcsh gawk \
	gnuplot netpbm libc6-i386


# Install
WORKDIR /home/
COPY ./netOglyc-3.1* /home/
RUN tar -xvzf netOglyc-3.1*.tar.gz
COPY ./signalp* /home/
RUN tar -xvzf signalp-5.0*.tar.gz
RUN cp signalp-5.0b/bin/* /usr/bin/
RUN cp signalp-5.0b/lib/* /usr/lib/
 

WORKDIR netOglyc-3.1/

# deal with some hard coded paths
RUN sed -i 's|/usr/cbs/packages/netOglyc/3.1/netOglyc-3.1d|/home/netOglyc-3.1|g' netOglyc		
RUN sed -i 's|/usr/cbs/bio/bin/signalp|/home/signalp-5.0b/bin/signalp|g' netOglyc

# update for signalp5 as other older versions are not available anymore...
RUN sed -i 's/$SIGNALP -t euk -m nn -trunc 60 -short infile.fsa | /signalp -org euk -format short -fasta infile.fas -prefix signalp.out; /g' netOglyc
RUN sed -i 's|grep -v '^#' |grep -v '^#' signalp.out*|g' netOglyc


# Create folders for input and output data
RUN mkdir -p /input
RUN mkdir -p /output

ENV PATH "$PATH:/home/netOglyc-3.1/"

# Setting working directory when docker image is running
WORKDIR /home/

