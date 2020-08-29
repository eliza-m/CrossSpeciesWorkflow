
################################################################################
#	DOCKERFILE
#	SCRATCH-1D v1.2 (SSpro & ACCpro 5) and DISpro 1.0
#
#	Link: 
#	http://scratch.proteomics.ics.uci.edu/
#
#	References:
#
#	C.N. Magnan & P. Baldi (2014). SSpro/ACCpro 5: almost perfect prediction 
#	of protein secondary structure and relative solvent accessibility using 
#	profiles, machine learning and structural similarity.Bioinformatics, vol 
#	30 (18), 2592-2597.
#
#	J. Cheng, A. Randall, M. Sweredoski, & P. Baldi. SCRATCH: a Protein 
#	Structure and Structural Feature Prediction Server. Nucleic Acids 
#	Research, vol. 33 (web server issue), w72-76, (2005).
#
#	J. Cheng, M. Sweredoski, & P. Baldi. Accurate Prediction of Protein 
#	Disordered Regions by Mining Protein Structure Data. Data Mining and 
#	Knowledge Discovery, vol. 11, no. 3, pp. 213-222, (2005).
#
################################################################################



# Start from 
FROM ubuntu:18.04

# Install packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils  \
		git build-essential cmake  \ 
		wget bash


		
# Set environment variables
ENV HOME=/home/
ENV MakeNoOfThreads=12


# Clone & Build SCRATCH-1D v1.2
WORKDIR /home/
RUN wget http://download.igb.uci.edu/SCRATCH-1D_1.2.tar.gz
RUN tar -xvzf SCRATCH-1D_1.2.tar.gz
RUN rm SCRATCH-1D_1.2.tar.gz

WORKDIR /home/SCRATCH-1D_1.2/
RUN perl install.pl

# The provided blast binaries are not compatible, therefore we replace them
WORKDIR /home/SCRATCH-1D_1.2/pkg/
RUN wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/legacy.NOTSUPPORTED/2.2.26/blast-2.2.26-x64-linux.tar.gz
RUN tar -xvzf blast-2.2.26-x64-linux.tar.gz
RUN rm blast-2.2.26-x64-linux.tar.gz
 

# TODO: DisPro seems to run with older version SSPRO4 (?!). Check if ok to use.
# http://download.igb.uci.edu/dispro1.0.tar.gz 

# Create folders for input and output data
RUN mkdir /input
RUN mkdir /output

COPY ./scratch1d_cwl.sh /home/

# Setting working directory when docker image is running
WORKDIR /home/


