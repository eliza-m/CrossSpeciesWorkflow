
################################################################################
#	DOCKERFILE
#	Disopred v3.1 using BLAST+
#
#	GitHub Repos: 
#	https://github.com/psipred/disopred
#
#	Reference: Jones, D.T. and Cozzetto, D. (2014) DISOPRED3: Precise 
#	disordered region predictions with annotated protein binding acrivity, 
#	Bioinformatics.
#
################################################################################



# Start from 
FROM ubuntu:18.04

# Install packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils \
		git build-essential cmake \ 
		wget bash tcsh ncbi-blast+


# Set environment variables
ENV DBname=uniref50.fasta
ENV DBfolder=/home/database/
ENV MakeNoOfThreads=4
ENV CPUnum=10

# Install some dependacies 
WORKDIR /home/
RUN wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/legacy.NOTSUPPORTED/2.2.26/blast-2.2.26-x64-linux.tar.gz
RUN tar -xvzf blast-2.2.26-x64-linux.tar.gz
RUN rm blast-2.2.26-x64-linux.tar.gz



##############################
#	Disopred
##############################


# Clone & Build the Disopred
WORKDIR /home/
RUN git clone --recursive https://github.com/psipred/disopred.git

WORKDIR /home/disopred/src/
RUN make clean
RUN make -j $MakeNoOfThreads
RUN make install

WORKDIR /home/
RUN wget http://bioinfadmin.cs.ucl.ac.uk/downloads/DISOPRED/dso_lib.tar.gz
RUN tar -zxvf dso_lib.tar.gz
ENV DSO_LIB_PATH=/home/dso_lib/

# setting up the hardcoded paths
# for legacy blast
WORKDIR /home/disopred/
RUN sed -i 's|my $NCBI_DIR = "/scratch0/NOT_BACKED_UP/dbuchan/Applications/blast-2.2.26/bin/";|my $NCBI_DIR = "/home/blast-2.2.26/bin/";|g' run_disopred.pl		
RUN sed -i 's|my $SEQ_DB = "/scratch0/NOT_BACKED_UP/dbuchan/uniref/uniref_test_db/uniref_test.fasta";|my $SEQ_DB = "$ENV{DBfolder}/$ENV{DBname}";|g' run_disopred.pl		

# for blast+
WORKDIR /home/disopred/BLAST+/
RUN sed -i 's|my $NCBI_DIR = "/scratch0/NOT_BACKED_UP/dbuchan/Applications/blast-2.2.26/bin/";|my $NCBI_DIR = "/usr/bin/";|g' run_disopred_plus.pl		
RUN sed -i 's|my $SEQ_DB = "/scratch0/NOT_BACKED_UP/dbuchan/uniref/uniref_test_db/uniref_test.fasta";|my $SEQ_DB = "$ENV{DBfolder}/$ENV{DBname}";|g' run_disopred_plus.pl		

# work around for path issues when using blast+ perl script...
RUN cp -r /home/disopred/bin .
RUN cp -f chkparse bin/chkparse
RUN ln -s /home/disopred/data data
RUN ln -s ${DSO_LIB_PATH} dso_lib


# make possible the usage of multiple CPU threads
RUN sed -i 's|"-num_alignments", "0",|"-num_alignments", "0", "-num_threads", "$ENV{CPUnum}",|g' run_disopred_plus.pl
RUN sed -i 's|">&", $hits_file;|">", $hits_file, "2>\&1";|g' run_disopred_plus.pl



# Create folders for input and output data
RUN mkdir /input
RUN mkdir /output


# Setting working directory when docker image is running
# messy workaround...to hijack all the relative paths issues...
ENV disopredplus="/home/disopred/BLAST+/run_disopred_plus.pl"

COPY ./disopredplus_cwl.sh /home/disopred/

WORKDIR /output/


################################################################################

