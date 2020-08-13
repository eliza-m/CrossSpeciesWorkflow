
################################################################################
#	DOCKERFILE
#	RaptorX - Property
#
#	GitHub Repos: 
#	https://github.com/realbigws/Predict_Property
#	https://github.com/realbigws/TGT_Package
#
#	References:
#
#	Wang, S.; Li, W.; Liu, S.; Xu, J. RaptorX-Property: a web server for 
#	protein structure property prediction. Nucleic Acids Res. 2016, 44, 
#	W430–W435.
#
#	Wang, S.; Peng, J.; Ma, J.; Xu, J. Protein Secondary Structure Prediction 
#	Using Deep Convolutional Neural Fields. Sci. Rep. 2016, 6, 1–11.
#
#	Wang, S.; Ma, J.; Xu, J. AUCpreD: Proteome-level protein disorder 
#	prediction by AUC-maximized deep convolutional neural fields. In 
#	Proceedings of the Bioinformatics; Oxford University Press, 2016; Vol. 
#	32, pp. i672–i679.
#	
#	Wang, S., Fei, S., Wang, Z., Li, Y., Xu, J., Zhao, F., Gao, X. PredMP: 
#	a web server for de novo prediction and visualization of membrane 
#	proteins.Bioinformatics, 2019; 35(4):691-693.
#
################################################################################


# Start from 
FROM ubuntu:18.04

# Install packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils \
		git build-essential cmake \ 
		wget bash

		
# Set environment variables
ENV HOME=/home/
ENV MakeNoOfThreads=12

# Clone & Build the RaptorX Predict_Property
WORKDIR /home/
RUN git clone --recursive https://github.com/realbigws/Predict_Property.git

WORKDIR /home/Predict_Property/source_code/
RUN make -j $MakeNoOfThreads


# Clone & Build the TGT_Package
WORKDIR /home/
RUN git clone --recursive https://github.com/realbigws/TGT_Package.git
RUN mkdir -p databases/

WORKDIR /home/TGT_Package/source_code/
RUN make -j $MakeNoOfThreads



# Optional if Jackhmmer does not work, you need to rebuild by uncommenting
# the next 2 lines :
# WORKDIR /home/TGT_Package/jackhmm/
# RUN ./install

# Optional if buildali2 does not work, you need to rebuild by uncommenting
# the next 2 lines :
# WORKDIR /home/TGT_Package/buildali2/source_code/
# RUN make -j $MakeNoOfThreads

# TODO: deal with HHsuite potentially occuring cpu "illegal instruction" 
# runtime error by rebuilding HHsuite !!!!!


# Create folders for input and output data
RUN mkdir /input
RUN mkdir /output

# Setting working directory when docker image is running
WORKDIR /home/

COPY ./raptorx_profile_cwl.sh /home/

################################################################################

