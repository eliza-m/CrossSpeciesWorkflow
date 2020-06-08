
################################################################################
#	DOCKERFILE
#	MusiteDeep - keras1 - theano - CPU based
#
#	MusiteDeep Repo: https://github.com/duolinwang/MusiteDeep
#
#	Reference: Duolin Wang, Shuai Zeng, Chunhui Xu, Wangren Qiu, Yanchun  
#	Liang, Trupti Joshi, Dong Xu, MusiteDeep: a Deep-learning Framework for 
#	General and Kinase-specific Phosphorylation Site Prediction, 
#	Bioinformatics 2017. 
################################################################################

# Start from 
FROM ubuntu:18.04

# Install packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils \
		git build-essential cmake \ 
		wget bash python-pip \
		#
		# not specified by MusiteDeep guys, but wierd errors appear 
		# in theano if not prior installed 
		libblas-dev liblapack-dev

		
# Clone & Build MusiteDeep
WORKDIR /home/
RUN git clone https://github.com/duolinwang/MusiteDeep.git

# Install dependancies
RUN pip install pandas numpy scipy h5py
RUN pip install -v keras==1.1.0
RUN pip install theano

# Workaround to make all imported modules work as intended
RUN touch /home/MusiteDeep/MusiteDeep/methods/__init__.py

# Create folders for input and output data
RUN mkdir /input
RUN mkdir /output

# Configure keras.json
RUN mkdir /home/.keras
RUN bash -c 'echo -e "{\n\x22image_dim_ordering\x22: \x22tf\x22,\n\x22epsilon\x22: 1e-07,\n\x22floatx\x22: \x22float32\x22,\n\x22backend\x22: \x22theano\x22\n}" > /home/.keras/keras.json'

# Setting working directory when docker image is running
WORKDIR /home/MusiteDeep/MusiteDeep/


################################################################################
