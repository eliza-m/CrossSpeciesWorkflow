
################################################################################
#	DOCKERFILE
#	DeepSUMO - CPU based
#
#	DeepSUMO Repo: https://github.com/zengyr49/DeepSumo
#
#	Reference:not found
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
RUN git clone https://github.com/zengyr49/DeepSumo.git

# Install dependancies
RUN pip3 install -v tensorflow==1.4.0 sklearn


# Create folders for input and output data
RUN mkdir /input
RUN mkdir /output

# Setting working directory when docker image is running
WORKDIR /home/DeepSumo/


################################################################################
