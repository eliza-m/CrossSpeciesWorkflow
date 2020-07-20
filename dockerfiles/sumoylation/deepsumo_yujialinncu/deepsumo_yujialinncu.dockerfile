
################################################################################
#	DOCKERFILE
#	DeepSUMO - CPU based
#
#	DeepSUMO Repo: https://github.com/yujialinncu/DeepSUMO
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
RUN git clone https://github.com/yujialinncu/DeepSUMO.git

# Install dependancies
RUN pip3 install pandas 
RUN pip3 install -v keras==2.2.2
RUN pip3 install -v tensorflow==1.5.0 

# Create folders for input and output data
RUN mkdir /input
RUN mkdir /output

# Setting working directory when docker image is running
WORKDIR /home/DeepSUMO/codes/


################################################################################
