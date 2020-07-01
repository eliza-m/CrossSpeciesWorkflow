
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
		wget bash python3-pip


# Set environment variables
ENV HOME=/home/
ENV MakeNoOfThreads=12


################################################################################
#	SPOT1D 
################################################################################

# Install dependancies
RUN pip3 install pandas numpy tqdm cPickle
RUN pip3 install -v tensorflow==1.4.0 


WORKDIR /home/
RUN wget https://servers.sparks-lab.org/downloads/SPOT-1D-local.tar.gz
RUN tar xzf SPOT-1D-local.tar.gz
RUN rm SPOT-1D-local.tar.gz

WORKDIR /home/SPOT-1D-local/

# Create folders for input and output data
RUN mkdir /input
RUN mkdir /output

# Setting working directory when docker image is running
WORKDIR /home/

################################################################################

