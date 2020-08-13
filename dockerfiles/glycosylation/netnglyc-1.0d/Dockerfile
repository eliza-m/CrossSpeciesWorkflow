
################################################################################
#	DOCKERFILE
#		
#	NetNglyc v1.0d :
#
#	Priorly running this dockerfile, it is required to access the above link
#	and consult the license agreement terms. If you are eligible to use
#	and download the software (indicated bellow) please register to DTU 
#	Health Tech and download and then copy inside the current directory
#	the following software :
#
#	Link : https://services.healthtech.dtu.dk/software.php
#
#	Additionally, NetNglyc uses SignalP software from DTU that needs to be 
#	downloaded from the above link and copied to the current directory.
#
#	References: R. Gupta, E. Jung and S. Brunak. Prediction of N-glycosylation sites in 
#	human proteins. In preparation, 2004.
#
################################################################################

# Start from 
FROM ubuntu:18.04

# Install packages
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils build-essential bash tcsh gawk \
	gnuplot netpbm libc6-i386


# Install & setup
WORKDIR /home/
COPY ./netNglyc* /home/
RUN tar -xvzf netNglyc*.tar.gz
COPY ./signalp* /home/
RUN tar -xvzf signalp-5.0*.tar.gz
RUN cp signalp-5.0b/bin/* /usr/bin/
RUN cp signalp-5.0b/lib/* /usr/lib/
 

WORKDIR netNglyc-1.0/

# deal with some hard coded paths
RUN sed -i 's|/usr/cbs/packages/netNglyc/1.0/netNglyc-1.0|/home/netNglyc-1.0|g' netNglyc		
RUN sed -i 's|/usr/cbs/bio/bin/signalp|/usr/bin/signalp|g' netNglyc

# update for signalp5 as other older versions are not available anymore...
RUN sed -i 's|$SIGNALP -t euk -m nn -trunc 60 -short|signalp -org euk -format short -fasta|g' netNglyc
RUN sed -i 's|>$GLYCTMP/signalp.out;|-prefix $GLYCTMP/signalp.out; mv $GLYCTMP/signalp.out* $GLYCTMP/signalp.out; |g' netNglyc



# Create folders for input and output data
RUN mkdir -p /input
RUN mkdir -p /output

ENV PATH "$PATH:/home/netNglyc-1.0/"

# Setting working directory when docker image is running
WORKDIR /home/

