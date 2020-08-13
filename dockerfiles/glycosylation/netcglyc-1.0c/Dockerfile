
################################################################################
#	DOCKERFILE
#		
#	NetCglyc v1.0 :
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
#	Karin Julenius. NetCGlyc 1.0: Prediction of mammalian C-mannosylation 
#	sites. Glycobiology, 17:868-876, 2007.
#	
################################################################################

# Start from 
FROM ubuntu:18.04

# Install packages
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y bash tcsh gawk 


# Install
WORKDIR /home/
COPY ./netCglyc-1.0* /home/
RUN zcat *.Z | tar -xvf -

WORKDIR netCglyc-1.0/
RUN mkdir -p /scratch

# deal with some hard coded paths
RUN sed -i 's|/usr/cbs/packages/netCglyc/1.0/|/home/|g' netCglyc		

# Create folders for input and output data
RUN mkdir -p /input
RUN mkdir -p /output

ENV PATH "$PATH:/home/netCglyc-1.0/"

# Setting working directory when docker image is running
WORKDIR /home/

