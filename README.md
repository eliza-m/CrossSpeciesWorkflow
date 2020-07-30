# Cross Species Structural, Post translational modifications and Functional protein predictions workflow

Content summary:
* [General Info](#general-info)
* [Project status](#project-status)
* [Prediction Modules - Installation & Usage](#prediction-modules-\--installation-and-usage)
* [CWL pipelines](#cwl-pipelines)
* [References](#references)

# General Info
While there are a multitude of open source ML methods for prediction of various structural or biological related attributes, there are no open source pipelines or APIs which allow to performing a one command task for running multiple/equivalent methods and join the results in a way that facilitates comparisons and further dissemination. This limits any type of structural/comparative biology analyses, as one would need to install and run >50 software and put together all the results using in-house scripts.

This project aims at developing a scalable workflow that receives the protein FASTA file and runs a series of structural and phenotype related predictors, generating a knowledge dataset that will facilitate further exploration and comparisons according to the following categories of features: secondary structure, solvent accessibility, disordered regions, PTS modifications (phosphorylation, glycosylation, lipid modification, sumoylation, etc) or binding sites.

Deliverables of this project consists of 8 modules for each analysis type organised as Docker images, a Python library for processing inputs & outputs of the included methods and bash and CWL pipelines that will facilitate a one-line command run of all the predictors (default or custom configuration).

This repo intends to create an easy, user accesible and open-source tool for running a series of third party predictions software. The main focus is on:
* Dockerfiles for easy installing existing prediction software.
* a Python API for facilitating parsing and organising each predictor's output data.
* bash and CWL pipelines that facilitates large protein sequences sets prediction jobs submissions.  


# Project status 
The project is currently under development :exclamation: :exclamation: :exclamation:. 
Some features might not won't work properly ::exclamation::

The project was tested so far only on native Ubuntu 18 .

Currently there are 3 main modules that deal with:
* A. Structural related predictors (secondary structure, relative solvent accesibility and intrinsical disorder regions predictions)
* B. Phosphorylation preditors
* C. Glycosylaytion predictors
* D. Acetylation predictors (:exclamation: on progress)
* E. Sumoylation predictors
* F. Cellular localisation predictors
* G. Lipid modification predictors (:exclamation: on progress)
* H. Miscellaneous predictors (:exclamation: on progress)


# Requirements before using CrossSpeciesWorkflow:

## Install Prerequisites
* Docker client: 
    * Docker Desktop for Windows or MAC - [click](https://www.docker.com/products/docker-desktop)
    * docker-ce-cli for Linux - [click](docs.docker.com/install/linux/docker-ce/ubuntu/)
* cwltool - [click](https://github.com/common-workflow-language/cwltool)
* Python3.8 and above


## Download some packages
Some of the 3rd party predictors require registering on their website prior downloading the software.

All DTU predictors are licensed only for for academic and non-profit usage and in order to download the software it is required to register on their website and accept the license agreement prior receiving via email a download link. Please register and download the bellow predictors (linux version as the dockerfile image is ubuntu based) from the [Download link](https://services.healthtech.dtu.dk/software.php)

* Phosphorylation module:
    * NetPhos
    * NetPhosPan
* Glycosylation module:
    * NetNGlyc
    * NetOGlyc
    * NetCGlyc
    * SignalP
 * Localisation module:
    * Tmhmm2

For these predictors it will be required to build your docker images using instructions bellow before using the CWL pipeline.



# CrossSpeciesWorkflow - Setup and Usage


## Clone repo
```
git clone https://github.com/eliza-m/CrossSpeciesWorkflow.git
```
Please set the CrossSpeciesWorkflow project home variable:
```
export CSW_HOME=/path/to/CrossSpeciesWorkflow/project/home
```

## Create docker images of the modules or individual predictors you are interested in. 

Please note that some of the predictors require registering on their website in order to download the source code. Also make sure that you have enough disk space available at the location were the docker image is being stored. 

```
# DTU predictors need registering before downloading the software !!!
# Please provide the path to the folder where DTU predictors source packages are being stored.

# Phosphorylation module
export netphospan_SOURCE=/path/to/netphospan/source
export netphos_SOURCE=/path/to/netphos/source

# Glycosylation module
export netcglyc_SOURCE=/path/to/netcglyc/source
export netoglyc_SOURCE=/path/to/netoglyc/source
export netnglyc_SOURCE=/path/to/netnglyc/source
export sinalp_SOURCE=/path/to/sinalp/source

# Localisation module
export tmhmm_SOURCE=/path/to/tmhmm/source
```

You can build only the docker images of the predictors you are interested in (please see bellow), or you can build all docker images by using the following bash script:
```
bash ${CSW_HOME}/bin/build_all_docker_images.sh
```

Some of the individual predictors require downloading and setting up different protein databases. Details of each predictors requirements and usage are shown in each predictors sections bellow :
* [RaptorX](### A1)
* [Psipred](### A2)
* [Disopred](### A3)

For testing that all the docker images work as expected, please set the following variables.

```
# input folder where FASTA file is located
export inputFolder=${CSW_HOME}/test/bash/single_protein/input

# protein name root ( in our example the FASTA file is 1pazA.fasta )
export prot="1pazA"

# output folder
export outputFolder=${CSW_HOME}/test/bash/single_protein/output

# CPU threads and maximum RAM (GB) to be used
export CPUnum=10
export maxRAM=16

# location of the protein database to be use for generatig sequence profiles
export RaptorxDBfolder=/path/to/uniprot20_2016_02

# for Psipred & DisoPred the recommended db is Uniref90 or Uniref50
export DBfolder=/path/to/uniref50
export DBname=uniref50.fasta
```

Alter setting the variables, you cand run the all modules test :
```
bash ${CSW_HOME}/test/bash/single_protein/test_ALL_modules.sh
```
If you are interested in a particular module only, separate tests are provided in ${CSW_HOME}/test/bash/single_protein/
In each predictor folder - `${outputFolder}/structural/scratch1d/expected_output/` samples of how the output should look are provided.


## Prediction Modules -  details & building individual docker images

## A. Structural module  

### A1. [RaptorX Protein Structure Property Prediction](http://raptorx.uchicago.edu/StructurePropertyPred/predict/) - from Xu group

The [RaptorX-Property repo](https://github.com/realbigws/RaptorX_Property_Fast) linked to the journal paper has been upgraded and split into 2 packages: 
* [Predict_Property - github repo & manual](https://github.com/realbigws/Predict_Property) 
* [TGT Package - github repo & manual](https://github.com/realbigws/TGT_Package)

Docker image contains:
* Secondary structure (SS) predictions (SS3 & SS8 - 3 and 8 classes classification) [\[WLLX 2016\]](#wllx-2016), [\[WPMX 2016\]](#wpmx-2016), [\[WSX 2016\]](#wsx-2016)
* Relative solvent accesibility (RSA) 
* Disorder prediction - AUCpreD [\[WMX 2016\]](#wmx-2016), [\[WSX 2016\]](#wsx-2016)
* Transmembrane topology - TopoPred (TM2 & TM8 - 2 and 8 classes classification) [\[WG 2019\]](#wg-2019)


Build docker image
```
cd ${CSW_HOME}/dockerfiles/structural/raptorx
docker build -t raptorx -f raptorx_property_cpu.dockerfile .
```

Get protein sequence database, according to the sequence profile generator sofware you want to use (installed in the docker image): 

* hhblits (default):
    *  uniprot20 (default) ~ 40 GB :
    http://wwwuser.gwdg.de/~compbiol/data/hhsuite/databases/hhsuite_dbs/old-releases/uniprot20_2016_02.tgz
    *  uniclust30 :
    http://wwwuser.gwdg.de/~compbiol/uniclust/2017_10/uniclust30_2017_10_hhsuite.tar.gz
    
* jackhmm :
    * uniref50 :
    ftp://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref50/uniref50.fasta.gz
    * uniref90 :
    ftp://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref90/uniref90.fasta.gz
  
* buildali2 :
    This should be mounted (or using simlinks) in "databases/nr_databases" (must contain nr90 and nr70).
    http://raptorx.uchicago.edu/download/
    
    
Usage example using bash :

For RaptorX the recommended db is uniprot20_2016_02 or uniclust30. For now, only the usage of uniprot20_2016_02 and hhsuite3 was tested. A sample of what the expected output should consist of is located in `${outputFolder}/structural/raptorx/expected_output/`.
```
# location of the protein database to be use for generatig sequence profiles
export RaptorxDBfolder=/storage1/eliza/protDBs/uniprot20_2016_02

docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/structural/raptorx:/output \
-v ${RaptorxDBfolder}:/home/TGT_Package/databases/uniprot20_2016_02 \
-e prot \
-e CPUnum \
-e maxRAM \
-it raptorx:latest bash -c '\
TGT_Package/A3M_TGT_Gen.sh -i /input/${prot}.fasta -h hhsuite3 -d uniprot20_2016_02 -c ${CPUnum} -m ${maxRAM} -o /output/; \
Predict_Property/Predict_Property.sh -i /output/${prot}.tgt -o /output/; '
```

<br /><br />

### A2. [SCRATCH-1D Protein Predictor v1.2 & DisPRO1.0](http://scratch.proteomics.ics.uci.edu/) - from Baldi group  

Links:
* [Website](http://scratch.proteomics.ics.uci.edu/)
* [Documentation](http://download.igb.uci.edu/SCRATCH-1D_documentation.txt); 
* [Installation guide](http://download.igb.uci.edu/SCRATCH-1D_readme.txt) 

Docker image contains 2 packages:
* SCRATCH-1D v1.2 [\[MB 2014\]](#mb-2014), [\[CRSB 2005\]](#crsb-2005) :
    * Secondary structure predictions (SSpro3 & SSpro8 - 3 and 8 classes classification) 
    * Relative solvent accesibility (ACCpro).
* DISpro1.0 Disorder prediction [\[CSB 2005\]](#csb-2005) 


Build docker image
```
cd ${CSW_HOME}/dockerfiles/structural/scratch1d
docker build -t scratch1d -f scratch1d.dockerfile .
```

Usage example using bash. A sample of what the expected output should consist of is located in `${outputFolder}/structural/scratch1d/expected_output/`.

```
docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/structural/scratch1d:/output \
-e prot \
-e CPUnum \
-it scratch1d:latest bash -c '\
SCRATCH-1D_1.2/bin/run_SCRATCH-1D_predictors.sh /input/${prot}.fasta /output/${prot} ${CPUnum} ;' 

```    


<br /><br />

### A3. [Psipred](http://bioinf.cs.ucl.ac.uk/psipred/) - from UCL Bioinformatics group  
Docker image contains:
* PSIPRED Protein Secondary Structure Predictor v4.0 ([github repo](https://github.com/psipred/psipred)) [\[BJ 2019\]](#bj-2019), [\[J 1999\]](#j-1999).
* DISOPRED Disorder Predictor v3.1 ([github repo](https://github.com/psipred/disopred)) [\[JC 2014\]](#jc-2014)

Build docker image:
```
cd ${CSW_HOME}/dockerfiles/structural/psipred
docker build -t psipred -f psipred.dockerfile .
```

This docker image will use BLAST+ for building the sequence profile. Therefore we need to download and setup a sequence database. Psipred recomands the usage of UniRef90. For more details visit their documentation (link above). Download UniRef50/UniRef90 in fasta format from [uniprot.org/downloads](https://www.uniprot.org/downloads).

Afterwards a blast database needs to be created (this steps need to be done only once, afterwards the database can be used or moved anywhere):
```
# if you do not habe BLAST+ installed run:
sudo apt-get install 
	
# go to the place where Uniref fasta file is being stored (change the path bellow accordingly):
cd /Place/where/UnirefX.fasta/file/is/stored
	
# create database (this might take a while from several minutes to one hour)
makeblastdb -dbtype prot -in uniref90.fasta
```

After the BLAST+ database has been generated, from now on we can use the docker image anytime.
Let's see an usage example using bash and also test that everything works as expected :

Let's set some custom variables:
	
The path to the folder where uniref is being stored (change it according to you case):
```
export DBfolder=/path/to/protDBs/uniref50
export DBname=uniref50.fasta	
```

Let's run Psipred ( no need to change anything as the variables used are being set above - just copy paste the whole command bellow ). Sample output for comparison is located in `${outputFolder}/structural/psipred/expected_output/`
```
docker run \
-v ${outputFolder}/structural/psipred:/output \
-v ${inputFolder}:/input \
-v ${DBfolder}:/home/database \
-e DBfolder=/home/database \
-e DBname \
-e prot \
-e CPUnum \
-it psipred:latest \
bash -c '\
cp /input/${prot}.fasta /output/ && cd /output/ ; \
$psipredplus /output/${prot}.fasta;'
```
<br /><br />


### A4. [Disopred](http://bioinf.cs.ucl.ac.uk/psipred/) - from UCL Bioinformatics group  
Docker image contains:
* DISOPRED Disorder Predictor v3.1 ([github repo](https://github.com/psipred/disopred)) [\[JC 2014\]](#jc-2014)

Build docker image:
```
cd ${CSW_HOME}/dockerfiles/structural/disopred 
docker build -t disopred -f disopred .dockerfile .
```

This docker image will use BLAST+ for building the sequence profile. Therefore we need to download and setup a sequence database. 
Please proceed as specified for Psipred (just above)

Let's run disopred ( no need to change anything as the variables used are being set above - just copy paste the whole command bellow ). Sample output for comparison is located in `${outputFolder}/structural/disopred/expected_output/`
```
docker run \
-v ${outputFolder}/structural/disopred:/output \
-v ${inputFolder}:/input \
-v ${DBfolder}:/home/database \
-e DBfolder=/home/database \
-e DBname \
-e prot \
-e CPUnum \
-it disopred:latest \
bash -c '\
cp /input/${prot}.fasta /output/ && cd /output/ ; \
$disopredplus /output/${prot}.fasta;'
```
<br /><br />



### A5. [SPOT-1D predictors](https://sparks-lab.org/server/spot-1d/) - from Sparks Lab  
SPOT-1D [\[HZ 2019\]](#hz-2019) is the updated version of Spider3 containing also additional features such as :
....

There are 2 available dokerfiles:
* CPU based
* GPU based

:exclamation: On progress


<br /><br />  

## B. Phosphorylation module :  

### B1. [NetPhos v3.1](https://services.healthtech.dtu.dk/service.php?NetPhos-3.1) predicts serine, threonine or tyrosine phosphorylation sites in eukaryotic proteins, either generic or kinase specific (17 kinases) [\[BGB 1999\]](#bgb-1999), [\[BB 2004\]](#bb-2004).

As all DTU predictors license is for academic and non-profit usage only, in order to download the software it is required to register on their website and accept the license agreement prior accessing the download page. Please register and download the above predictors (linux version as the dockerfile image is ubuntu based) from the [Download link](https://services.healthtech.dtu.dk/software.php)

After you complete the license agreement and download the software, you can proceed building the docker image:
```
cd ${CSW_HOME}/dockerfiles/phosphorylation/netphos-3.1
cp ${netphos_SOURCE}/netphos-3.1* ${CSW_HOME}/dockerfiles/phosphorylation/netphos-3.1/
docker build -t netphos-3.1 -f netphos-3.1.dockerfile .     
```

Let's run NetPhos3.1 ( no need to change anything as the variables used are being set above - just copy paste the whole command bellow )
```
docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/phosphorylation/netphos:/output \
-e prot \
-it netphos-3.1:latest \
bash -c '\
/home/netphos-3.1/ape-1.0/ape /input/${prot}.fasta > /output/${prot}.netphos.out; '
```

### B2. [NetPhospan v1.0](https://services.healthtech.dtu.dk/service.php?NetPhospan-1.0) predicts phophorylation sites from a set of 120 human kinase [\[FN 2018\]](#fn-2018).

As all DTU predictors license is for academic and non-profit usage only, in order to download the software it is required to register on their website and accept the license agreement prior accessing the download page. Please register and download the above predictors (linux version as the dockerfile image is ubuntu based) from the [Download link](https://services.healthtech.dtu.dk/software.php)

After you complete the license agreement and download the software, you can proceed building the docker image:
```
cd ${CSW_HOME}/dockerfiles/phosphorylation/netphospan-1.0
cp ${netphospan_SOURCE}/netphospan-1.0* ${CSW_HOME}/dockerfiles/phosphorylation/netphospan-1.0/
docker build -t netphospan-1.0 -f netphospan-1.0.dockerfile .     
```


Let's run now NetPhospan for this protein example, using either the generic predictor (`-generic` flag), or a kinase specific model (`-a kinasename`). For a list of supported kinase models please see the documentation for this predictor :

```
# General predictor :
docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/phosphorylation/netphospan:/output \
-e prot=$prot \
-it netphospan-1.0:latest \
bash -c '\
netphospan-1.0.Linux/netphospan -f /input/${prot}.fasta -generic > /output/${prot}.generic.netphospan.out;'

# Kinase specific :
docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/phosphorylation/netphospan:/output \
-e prot=$prot \
-it netphospan-1.0:latest \
bash -c '\
netphospan-1.0.Linux/netphospan -f /input/${prot}.fasta -a PKACA > /output/${prot}.PKACA.netphospan.out;'
```

<br /><br />


### B3. [MusiteDeep Phosphorylation predictors](https://www.musite.net/) 

MusiteDeep Phosphorylation ([github repo](https://github.com/duolinwang/MusiteDeep)) predicts general and/or kinase specific phosphorylation sites [\[WX 2017\]](#wx-2017). 

There are 4 available dokerfiles:
* MusiteDeep using Keras1 and Theano CPU-based
* MusiteDeep using Keras2 and Tensorflow CPU-based - which is much faster than Theano's version

According to your choice, build the selected docker image:
```
cd ${CSW_HOME}/dockerfiles/phosphorylation/musitedeep

docker build -t musitedeep_keras2_tensorflow_cpu -f musitedeep_keras2_tensorflow_cpu.dockerfile .
docker build -t musitedeep_keras1_theano_cpu -f musitedeep_keras1_theano_cpu.dockerfile .
```

Let's see an usage example using bash and also test that everything works as expected. We will use the variables set above.

MusiteDeep contains a generic phosphorylation predictor, as well as trained kinase specific models (only for 'CDK','PKA','CK2', 'MAPK', 'PKC' kinases). Additionally it provides some custom models and the possibility to train custom models based on users data. Please see their documentation for detailed usage info.

Using MusiteDeep v1.0 (theano) : 

Either the general predictor :
```
docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/phosphorylation/musitedeep_keras1_theano:/output \
-e prot \
-it musitedeep_keras1_theano_cpu:latest \
bash -c '\
python predict.py -input /input/${prot}.fasta -output /output/ \
-predict-type general -residue-types S,T,Y ;'
```

Or kinase specific:
```
docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/phosphorylation/musitedeep_keras1_theano:/output \
-e prot \
-it musitedeep_keras1_theano_cpu:latest \
bash -c '\
python predict.py -input /input/${prot}.fasta -output /output/ \
-predict-type kinase -kinase CDK ;'
```

Similarly for MusiteDeep v2.0 (tensorflow), only the image name needs to be change and the usage is almost equivalent : 

For the general predictor :
```
docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/phosphorylation/musitedeep_keras2_tensorflow:/output \
-e prot \
-it musitedeep_keras2_tensorflow_cpu:latest \
bash -c '\
python predict.py -input /input/${prot}.fasta -output /output/ \
-predict-type general -residue-types S,T,Y ;'
```
Or Kinase specific :
```
docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/phosphorylation/musitedeep_keras2_tensorflow:/output \
-e prot \
-it musitedeep_keras2_tensorflow_cpu:latest \
bash -c '\
python predict_batch.py -input /input/${prot}.fasta -output /output/ \
-predict-type kinase -kinase CDK ;'
```

<br /><br />

    
## C. Glycosylation module
  
### C1. [NetNGlyc v1.0](https://services.healthtech.dtu.dk/service.php?NetNGlyc-1.0) 
Predicts N-Glycosylation sites in human proteins [\[GJB 2004\]](#gjb-2004). [CLI user guide](http://www.cbs.dtu.dk/cgi-bin/nph-runsafe?man=netNglyc)

As all DTU predictors license is for academic and non-profit usage only, in order to download the software it is required to register on their website and accept the license agreement prior accessing the download page. Please register and download the above predictors (linux version as the dockerfile image is ubuntu based) from the [Download link](https://services.healthtech.dtu.dk/software.php)

After you complete the license agreement and download the software, you can proceed building the docker image:
```
cd ${CSW_HOME}/dockerfiles/phosphorylation/netnglyc-1.0d
cp ${netnglyc_SOURCE}/netnglyc-1* ${CSW_HOME}/dockerfiles/phosphorylation/netnglyc-1.0d/
cp ${signalp_SOURCE}/signalp* ${CSW_HOME}/dockerfiles/phosphorylation/netnglyc-1.0d/
docker build -t netnglyc-1.0d -f netnglyc-1.0d.dockerfile . 
```

Let's run NetNglyc ( no need to change anything as the variables used are being set above - just copy paste the whole command bellow )
```
docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/glycosylation/netnglyc:/output \
-e prot \
-it netnglyc-1.0d:latest \
bash -c '\
netNglyc /input/${prot}.fasta > /output/${prot}.netnglyc.out; '
```

<br /><br />


### C2. [NetOGlyc v4.0](https://services.healthtech.dtu.dk/service.php?NetOGlyc-4.0) 
Predicts O-GalNAc (mucin type) glycosylation sites in mammalian proteins. [\[SC 2013\]](#sc-2013):

As all DTU predictors license is for academic and non-profit usage only, in order to download the software it is required to register on their website and accept the license agreement prior accessing the download page. Please register and download the above predictors (linux version as the dockerfile image is ubuntu based) from the [Download link](https://services.healthtech.dtu.dk/software.php)

After you complete the license agreement and download the software, you can proceed building the docker image:
```
cd ${CSW_HOME}/dockerfiles/phosphorylation/netoglyc-3.1
cp ${netoglyc_SOURCE}/netoglyc-3.1* ${CSW_HOME}/dockerfiles/phosphorylation/netoglyc-3.1/
cp ${signalp_SOURCE}/signalp* ${CSW_HOME}/dockerfiles/phosphorylation/netoglyc-3.1/
docker build -t netoglyc-3.1 -f netoglyc-3.1.dockerfile .
```

Let's run NetOglyc ( no need to change anything as the variables used are being set above - just copy paste the whole command bellow )
```
docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/glycosylation/netoglyc:/output \
-e prot \
-it netoglyc-3.1:latest \
bash -c '\
netOglyc /input/${prot}.fasta > /output/${prot}.netoglyc.out; '
```

<br /><br />

### C3. [NetCGlyc v1.0](http://www.cbs.dtu.dk/services/NetCGlyc/) 
Predicts tryptophan C-mannosylation sites in mammalian proteins [\[J 2007\]](#j-2007).

As all DTU predictors license is for academic and non-profit usage only, in order to download the software it is required to register on their website and accept the license agreement prior accessing the download page. Please register and download the above predictors (linux version as the dockerfile image is ubuntu based) from the [Download link](https://services.healthtech.dtu.dk/software.php)

After you complete the license agreement and download the software, you can proceed building the docker image:
```
cd ${CSW_HOME}/dockerfiles/phosphorylation/netcglyc-1.0c
cp ${netcglyc_SOURCE}/netcglyc-1* ${CSW_HOME}/dockerfiles/phosphorylation/netcglyc-1.0c/
docker build -t netcglyc-1.0c -f netcglyc-1.0c.dockerfile . 
```

Let's run NetCglyc ( no need to change anything as the variables used are being set above - just copy paste the whole command bellow )
```
docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/glycosylation/netcglyc:/output \
-e prot \
-it netcglyc-1.0c:latest \
bash -c '\
netCglyc /input/${prot}.fasta > /output/${prot}.netcglyc.out; '
```

<br /><br />
    
### C4. [ISOGlyP](https://isoglyp.utep.edu/) 
Predicts isoform specific mucin-type o-glycosylation sites [\[ML 2020\]](#\ml-2020).
Github repo - https://github.com/jonmohl/ISOGlyP

Building the docker image:
```
cd ${CSW_HOME}/dockerfiles/phosphorylation/isoglyp
docker build -t isoglyp -f isoglyp.dockerfile . 
```

Let's run ISOGlyP ( no need to change anything as the variables used are being set above - just copy paste the whole command bellow )
```
docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/glycosylation/isoglyp:/output \
-e prot \
-it isoglyp \
bash -c '\
isoglypCL.py -p /home/ISOGlyP/isoPara.txt -f /input/${prot}.fasta ; \
mv isoglyp-predictions.csv /output/${prot}.isoglyp.out; '
```

<br /><br />

## D. Acetylation module :  
:exclamation: On progress...


<br /><br />

## E. Sumoylation module :  

### E1. [DeepSumo from Ren Lab](http://deepsumo.renlab.org/) 
Predicts protein SUMOylation sites and SUMO-interaction motifs by deep learning [no refference found] 
Github repo - https://github.com/zengyr49/DeepSumo

Building the docker image:
```
cd ${CSW_HOME}/dockerfiles/sumoylation/deepsumo_ren
docker build -t deepsumo_ren -f deepsumo_ren.dockerfile . 
```

Let's run DeepSumo ( no need to change anything as the variables used are being set above - just copy paste the whole command bellow )
```
docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/sumoylation/deepsumo_ren:/output \
-e prot \
-e thresh_sumo="low" \
-e thresh_sim="low" \
-it deepsumo_ren:latest \
bash -c '\
python3 predict_main.py --t1 $thresh_sumo --t2 $thresh_sim \
-i /input/${prot}.fasta -o /output/ '
```

<br /><br />


### E2. [DeepSUMO]
Predicts lysine SUMOylation sites by conv nets [no refference found]
Github repo - https://github.com/loneMT/DeepSUMO && https://github.com/yujialinncu/DeepSUMO

Building the docker image:
```
cd ${CSW_HOME}/dockerfiles/sumoylation/deepsumo_yl
docker build -t deepsumo_yl -f deepsumo_yl.dockerfile . 
```

Let's run DeepSUMO ( no need to change anything as the variables used are being set above - just copy paste the whole command bellow )
```
docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/sumoylation/deepsumo_yl:/output \
-e prot \
-it deepsumo_yl:latest \
bash -c '\
python3 /home/DeepSUMO/codes/predict.py -input /input/${prot}.fasta \
-threshold 0.5 -output /output/${prot}.deepsumo_yl.out;'
```
<br /><br />


## F. Cellular localisation module :  

### F1. [TMP-SSurface](http://deepsumo.renlab.org/) 
Predicts RSA for transmembrane proteins using deep learning [\[LW 2019\]](#lw-2019)
Github repo - https://github.com/Liuzhe30/TMP-SSurface-2.0

Building the docker image:
```
cd ${CSW_HOME}/dockerfiles/localisation/tmp_ssurface
docker build -t tmp_ssurface -f tmp_ssurface.dockerfile . 
```

Let's run TMP-SSurface ( no need to change anything as the variables used are being set above - just copy paste the whole command bellow )
```
docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/localisation/tmp_ssurface:/output \
-e prot \
-it tmp_ssurface:latest \
bash -c '\
python3 run.py -f /input/${prot}.fasta -p /input/pssm/ -o /output/ ;'
```
<br /><br />


### F2. [TMHMM v2.0](http://www.cbs.dtu.dk/services/TMHMM/) 
Predicts transmembrane helices [\[KS 2001\]](#ks-2001)

As all DTU predictors license is for academic and non-profit usage only, in order to download the software it is required to register on their website and accept the license agreement prior accessing the download page. Please register and download the above predictors (linux version as the dockerfile image is ubuntu based) from the [Download link](https://services.healthtech.dtu.dk/software.php)

After you complete the license agreement and download the software, you can proceed building the docker image:
```
cd ${CSW_HOME}/dockerfiles/localisation/tmhmm2
cp ${tmhmm_SOURCE}/tmhmm-2.0c* ${CSW_HOME}/dockerfiles/localisation/tmhmm2/
docker build -t tmhmm2 -f tmhmm2.dockerfile . 
```
Let's run TMHMM ( no need to change anything as the variables used are being set above - just copy paste the whole command bellow )
```
docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/localisation/tmhmm2:/output \
-e prot \
-it tmhmm2:latest \
bash -c '\
tmhmm /input/${prot}.fasta > /output/${prot}.tmhmm2.out; \
cp TMHMM_*/* /output/;'
```
<br /><br />


### F3. [MEMSAT-SVM](http://bioinf.cs.ucl.ac.uk/psipred/) 
Predicts transmembrane regions and cellular localisation [\[NJ 2009\]](#nj-2009)
Github repo - https://github.com/psipred/MemSatSVM

Building the docker image:
```
cd ${CSW_HOME}/dockerfiles/localisation/memsatsvm
docker build -t memsatsvm -f memsatsvm.dockerfile . 
```

Let's run MEMSAT-SVM ( no need to change anything as the variables used are being set above - just copy paste the whole command bellow )
```
docker run \
-v ${inputFolder}:/input \
-v ${outputFolder}/localisation/memsatsvm:/output \
-e prot \
-it memsatsvm:latest \
bash -c '\
./run_memsat-svm.pl -p 1 -g 0 -mtx 1 /input/pssm_mtx/${prot}.mtx -j /output/'
```
<br /><br />


## G. Miscellaneous module :  
:exclamation: On progress...

<br /><br />  




# CWL pipelines
:exclamation: On progress






# References  

### Structural predictors:

##### \[WLLX 2016\]
Wang, S.; Li, W.; Liu, S.; Xu, J. RaptorX-Property: a web server for protein structure property prediction. Nucleic Acids Res. 2016, 44, W430–W435.
##### \[WPMX 2016\] 
Wang, S.; Peng, J.; Ma, J.; Xu, J. Protein Secondary Structure Prediction Using Deep Convolutional Neural Fields. Sci. Rep. 2016, 6, 1–11.
##### \[WMX 2016\] 
Wang, S.; Ma, J.; Xu, J. AUCpreD: Proteome-level protein disorder prediction by AUC-maximized deep convolutional neural fields. In Proceedings of the Bioinformatics; Oxford University Press, 2016; Vol. 32, pp. i672–i679.
##### \[WSX 2016\] 
Wang, S.; Sun, S.; Xu, J. AUC-maximized deep convolutional neural fields for protein sequence labeling. In Proceedings of the Lecture Notes in Computer Science (including subseries Lecture Notes in Artificial Intelligence and Lecture Notes in Bioinformatics); Springer Verlag, 2016; Vol. 9852 LNAI, pp. 1–16.
##### \[WG 2019\] 
Wang, S., Fei, S., Wang, Z., Li, Y., Xu, J., Zhao, F., Gao, X. PredMP: a web server for de novo prediction and visualization of membrane proteins.Bioinformatics, 2019; 35(4):691-693. doi: 10.1093/bioinformatics/bty684.
##### \[SS 2019\] 				
Steinegger M, Meier M, Mirdita M, Vöhringer H, Haunsberger S J, and Söding J (2019) HH-suite3 for fast remote homology detection and deep protein annotation, BMC Bioinformatics, 473. doi: 10.1186/s12859-019-3019-7
##### \[MB 2014\] 
C.N. Magnan & P. Baldi (2014). SSpro/ACCpro 5: almost perfect prediction of protein secondary structure and relative solvent accessibility using profiles, machine learning and structural similarity.Bioinformatics, vol 30 (18), 2592-2597.
##### \[CRSB 2005\] 
J. Cheng, A. Randall, M. Sweredoski, & P. Baldi. SCRATCH: a Protein Structure and Structural Feature Prediction Server.
Nucleic Acids Research, vol. 33 (web server issue), w72-76, (2005).
##### \[CSB 2005\] 
J. Cheng, M. Sweredoski, & P. Baldi. Accurate Prediction of Protein Disordered Regions by Mining Protein Structure Data. Data Mining and Knowledge Discovery, vol. 11, no. 3, pp. 213-222, (2005).
##### \[JC 2014]
Jones, D.T. and Cozzetto, D. (2014) DISOPRED3: Precise disordered region predictions with annotated protein binding acrivity, Bioinformatics.
##### \[BJ 2019]
Buchan DWA, Jones DT (2019). The PSIPRED Protein Analysis Workbench: 20 years on. Nucleic Acids Research. https://doi.org/10.1093/nar/gkz297
##### \[J 1999]
Jones DT. (1999) Protein secondary structure prediction based on position-specific scoring matrices. J. Mol. Biol. 292: 195-202.
##### \[HZ 2019]
Hanson, J., Paliwal, K., Litfin, T., Yang, Y., & Zhou, Y. (2019). Improving prediction of protein secondary structure, backbone angles, solvent accessibility and contact numbers by using predicted contact maps and an ensemble of recurrent and residual convolutional neural networks. Bioinformatics (Oxford, England), 35(14), 2403–2410. https://doi.org/10.1093/bioinformatics/bty1006  


<br /><br />

### Phosphorylation predictors:

##### \[BGB 1999]
Blom, N., Gammeltoft, S., and Brunak, S. Sequence- and structure-based prediction of eukaryotic protein phosphorylation sites. Journal of Molecular Biology: 294(5): 1351-1362, 1999.
##### \[BB 2004]
Blom N, Sicheritz-Ponten T, Gupta R, Gammeltoft S, Brunak S. Prediction of post-translational glycosylation and phosphorylation of proteins from the amino acid sequence. Proteomics: Jun;4(6):1633-49, review 2004.
##### \[FN 2018]
Emilio Fenoy, Jose M. G. Izarzugaza, Vanessa Jurtz, Søren Brunak and Morten Nielsen. A generic Deep Convolutional Neural Network framework for prediction of Receptor-ligand Interactions. NetPhosPan; Application to Kinase Phosphorylation prediction.
Bioinformatics (2018).
##### \[WX 2017]
Duolin Wang, Shuai Zeng, Chunhui Xu, Wangren Qiu, Yanchun Liang, Trupti Joshi, Dong Xu, MusiteDeep: a Deep-learning Framework for General and Kinase-specific Phosphorylation Site Prediction, Bioinformatics 2017.


<br /><br />

### Glycosylation predictors:

##### \[GJB 2004]
R. Gupta, E. Jung and S. Brunak. Prediction of N-glycosylation sites in human proteins. In preparation, 2004.
##### \[SC 2013]
Steentoft C, Vakhrushev SY, Joshi HJ, Kong Y, Vester-Christensen MB, Schjoldager KT, Lavrsen K, Dabelsteen S, Pedersen NB, Marcos-Silva L, Gupta R, Bennett EP, Mandel U, Brunak S, Wandall HH, Levery SB, Clausen H. Precision mapping of the human O-GalNAc glycoproteome through SimpleCell technology. EMBO J, 32(10):1478-88, 2013. doi: 10.1038/emboj.2013.79
##### \[G 2001]
R Gupta. Prediction of glycosylation sites in proteomes: from post-translational modifications to protein function. Ph.D. thesis at CBS, 2001.
##### \[GB 2002]
Gupta, R. and S. Brunak. Prediction of glycosylation across the human proteome and the correlation to protein function. Pacific Symposium on Biocomputing, 7:310-322, 2002.
##### \[J 2007]
Karin Julenius. NetCGlyc 1.0: Prediction of mammalian C-mannosylation sites. Glycobiology, 17:868-876, 2007.  
##### \[ML 2020]
Mohl JE, Gerken TA, Leung MY. ISOGlyP: de novo prediction of isoform specific mucin-type O-glycosylation [published online ahead of print, 2020 Jul 15]. Glycobiology. 2020;cwaa067. doi:10.1093/glycob/cwaa067


<br /><br />

### Acetylation predictors:

<br /><br />

### Sumoylation predictors:

<br /><br />

### Celullar localisation predictors:
##### \[LW 2019]
Lu, C.; Liu, Z.; Kan, B.; Gong, Y.; Ma, Z.; Wang, H. TMP-SSurface: A Deep Learning-Based Predictor for Surface Accessibility of Transmembrane Protein Residues. Crystals 2019, 9, 640.
##### \[KS 2001]
Krogh A, Larsson B, von Heijne G, Sonnhammer EL. Predicting transmembrane protein topology with a hidden Markov model: application to complete genomes. J Mol Biol. 2001;305(3):567-580. doi:10.1006/jmbi.2000.4315
##### \[NJ 2009]
Nugent, T. & Jones, D.T. (2009) Transmembrane protein topology prediction using support vector machines. BMC Bioinformatics. 10, 159. Epub


<br /><br />

### Miscellaneous predictors:

<br /><br />
