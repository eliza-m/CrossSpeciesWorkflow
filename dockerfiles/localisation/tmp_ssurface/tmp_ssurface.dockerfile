
################################################################################
#	DOCKERFILE
#	TMP-SSurface - CPU based
#
#	TMP-SSurface Repo: https://github.com/Liuzhe30/TMP-SSurface-2.0.git
#
#	Reference:  C. Lu, Z. Liu, B. Kan, Y. Gong, Z. Ma and H. Wang, 
#	"TMP-SSurface: A deep learning-based predictor for surface accessibility 
#	of transmembrane protein residues", Crystals, vol. 9, no. 12, pp. 640, 
#	Dec. 2019.
# 
################################################################################

# Start from 
FROM ubuntu:18.04

# Install packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils \
		git build-essential \ 
		wget bash python3-pip

ENV HOME=/home/

# Clone
WORKDIR /home/
RUN git clone https://github.com/Liuzhe30/TMP-SSurface-2.0.git

# Install dependancies

RUN pip3 install --upgrade pip
RUN pip3 install tensorflow==2.0 keras==2.3 matplotlib


# Create folders for input and output data
RUN mkdir /input
RUN mkdir /output

# Setting working directory when docker image is running
WORKDIR /home/TMP-SSurface-2.0/TMP-SSurface-2.0

# workaround for CWL
COPY ./tmp_ssurface_cwl.sh /home/


################################################################################
