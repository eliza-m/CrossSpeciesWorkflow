
################################################################################
#	DOCKERFILE
#		
#	ISOGlyP :
#
#	Github repo : https://github.com/jonmohl/ISOGlyP.git
#
#	References: Jonathon E Mohl, Thomas A Gerken, Ming-Ying Leung, ISOGlyP: 
#	de novo prediction of isoform specific mucin-type O-glycosylation, 
#	Glycobiology, , cwaa067, https://doi.org/10.1093/glycob/cwaa067
#
################################################################################

# Start from 
FROM ubuntu:18.04

# Install packages
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils build-essential git bash python3


# Clone & setup project
WORKDIR /home/
RUN git clone https://github.com/jonmohl/ISOGlyP.git
RUN git clone https://github.com/jonmohl/ISOGlyP-EV_Tables.git


ENV PATH "$PATH:/home/ISOGlyP/"

RUN sed -i 's|evd=~/github/|evd=/home/|g' ISOGlyP/isoPara.txt


# Create folders for input and output data
RUN mkdir -p /input
RUN mkdir -p /output

# Setting working directory when docker image is running
WORKDIR /output