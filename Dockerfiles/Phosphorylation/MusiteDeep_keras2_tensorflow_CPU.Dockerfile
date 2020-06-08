
################################################################################
#	DOCKERFILE
#	MusiteDeep - keras2 - tensorflow - CPU based
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
		libblas-dev liblapack-dev


# Clone & Build MusiteDeep
WORKDIR /home/
RUN git clone https://github.com/duolinwang/MusiteDeep.git

# Install dependancies
RUN pip install pandas numpy scipy h5py
RUN pip install -v keras==2.1.2
RUN pip install -v tensorflow==1.3.0 

# Workaround to make all the imported modules work as intended
RUN touch /home/MusiteDeep/MusiteDeep_Keras2.0/MusiteDeep/methods/__init__.py

# Create folders for input and output data
RUN mkdir /input
RUN mkdir /output

# Configure keras.json
RUN mkdir /home/.keras
RUN bash -c 'echo -e "{\n\x22image_dim_ordering\x22: \x22th\x22,\n\x22epsilon\x22: 1e-07,\n\x22floatx\x22: \x22float32\x22,\n\x22backend\x22: \x22tensorflow\x22\n}" > /home/.keras/keras.json'

# Setting working directory when docker image is running
WORKDIR /home/MusiteDeep/MusiteDeep_Keras2.0/MusiteDeep/

# COMMENT: the standard version of tensorflow does not use all the common 
# compiler flags.. it could be recompiled to use SSE4.2, AVX, etc... 
# however, as the prediction takes only a few seconds per protein sequence...  
# maybe this is not a priority :)

################################################################################
