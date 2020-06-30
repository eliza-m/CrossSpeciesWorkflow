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
The project is currently under development ::exclamation:: ::exclamation:: ::exclamation::. 
Many features in this devevelopment branch are not yet implemented and won't work properly ::exclamation::

Currently there are 3 main modules that deal with:
* Structural related predictors (secondary structure, relative solvent accesibility and intrinsical disorder regions predictions)
* Glycosylaytion predictors
* Phosphorylation


# Prediction Modules - Installation and Usage


## Install prerequisites:

* Docker client: 
    * Docker Desktop for Windows or MAC - [click](https://www.docker.com/products/docker-desktop)
    * docker-ce-cli for Linux - [click](docs.docker.com/install/linux/docker-ce/ubuntu/)
* cwltool - [click](https://github.com/common-workflow-language/cwltool)
* Python3

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

You can build only the docker images of the predictors you are interested in (please see bellow), or you can build all docker images by using the following bash script:
```
bash ${CSW_HOME}/bin/build_all_docker_images.sh
```
Some of the individual predictors require downloading and setting up different protein databases. Details of each predictors requirements and usage are shown in the sections bellow :

## Prediction Modules 

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
docker build -t raptorx_property_cpu -f raptorx_property_cpu.dockerfile .
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

```
# for RaptorX the recommended db is uniprot20_2016_02 or uniclust30. For now, only the usage of uniprot20_2016_02 and hhsuite3 was tested.
export RaptorxProtDB_NAME=uniprot20_2016_02

# location of the protein database to be use for generatig sequence profiles
export RaptorxProtDB_PATH=/storage1/eliza/protDBs/uniprot20_2016_02


# input folder where FASTA file is located
export inputFolder=${CSW_HOME}/test/input

# protein name root ( in our example the FASTA file is 1pazA.fasta )
export prot="1pazA"

# output folder
export outputFolder=${CSW_HOME}/test/output

# CPU threads and maximum RAM (GB) to be used
export CPUnum=10
export maxRAM=4


docker run \
-v ${RaptorxProtDB_PATH}:/home/TGT_Package/databases/uniprot20_2016_02 \
-v ${outputFolder}:/output \
-v ${inputFolder}:/input \
-e prot \
-e CPUnum \
-e maxRAM \
-it raptorx_property_cpu:latest bash -c '\
mkdir -p /output/${prot}; \
mkdir -p /output/${prot}/RaptorX; \
TGT_Package/A3M_TGT_Gen.sh -i /input/${prot}.fasta -h hhsuite3 -d uniprot20_2016_02 -c ${CPUnum} -m ${maxRAM} -o /output/${prot}/RaptorX/${prot}_A3MTGT; \
Predict_Property/Predict_Property.sh -i /output/${prot}/RaptorX/${prot}_A3MTGT/${prot}.tgt -o /output/${prot}/RaptorX/${prot}_PROP; '\

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
docker build -t scratch1d_cpu -f scratch1d_cpu.dockerfile .
```

Usage example using bash :

```
# input folder where FASTA file is located
export inputFolder=${CSW_HOME}/test/input

# protein name root ( in our example the FASTA file is 1pazA.fasta )
export prot="1pazA"

# output folder
export outputFolder=${CSW_HOME}/test/output

# CPU threads to be used
export CPUnum=10

docker run \
-v ${outputFolder}:/output \
-v ${inputFolder}:/input \
-e prot \
-e CPUnum \
-it scratch1d_cpu:latest bash -c '\
mkdir -p output/${prot}; \
mkdir -p output/${prot}/Scratch1D; \
SCRATCH-1D_1.2/bin/run_SCRATCH-1D_predictors.sh /input/${prot}.fasta /output/${prot}/Scratch1D/${prot} ${CPUnum} ;' 

```    


<br /><br />

### A3. [Psipred predictors](http://bioinf.cs.ucl.ac.uk/psipred/) - from UCL Bioinformatics group  
Docker image contains 2 packages:
* PSIPRED Protein Secondary Structure Predictor v4.0 ([github repo](https://github.com/psipred/psipred)) [\[BJ 2019\]](#bj-2019), [\[J 1999\]](#j-1999).
* DISOPRED Disorder Predictor v3.1 ([github repo](https://github.com/psipred/disopred)) [\[JC 2014\]](#jc-2014)

Build docker image:
```
cd ${CSW_HOME}/dockerfiles/structural/psipred_disopred
docker build -t psipred_disopred_cpu -f psipred_disopred_cpu.dockerfile .
```

This docker image will use BLAST+ for building the sequence profile. Therefore we need to download and setup a sequence database. Psipred recomands the usage of UniRef90. For more details visit their documentation (link above). Download UniRef90 in fasta format from [uniprot.org/downloads](https://www.uniprot.org/downloads).

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
export PsipredProtDB_PATH=/storage1/eliza/protDBs/uniref90
```

The name of the uniref fasta file (in case you wish to use uniref50 or other database)
```
export PsipredProtDB_NAME=uniref90
```
	
The number of CPU threads to be used when using psiblast
```
export CPUnum=4
```
	
Specify the folder where the input fasta files are. We will use the provided examples in this repo.
```
export inputFolder=${CSW_HOME}/test/input
```

Specify the protein root name (in our example the fasta file is "1pazA.fasta"):
```
export prot="1pazA"
```

Set an output folder there the results will be generated. We will in this repo.
```
export outputFolder=${CSW_HOME}/test/output
```


Let's run Psipred ( no need to change anything as the variables used are being set above - just copy paste the whole command bellow )
```
docker run \
-v ${PsipredProtDB_PATH}:/home/database/ \
-e ${PsipredProtDB_NAME}=${uniref_fastafile} \
-v ${outputFolder}:/output \
-v ${inputFolder}:/input \
-e prot=$prot \
-e RunNumOfThreads=$CPUnum \
-it psipred_disopred_cpu:latest \
bash -c '\
mkdir -p ${prot}; \
mkdir -p ${prot}/PsiPred; \
cp /input/${prot}.fasta /output/${prot}/PsiPred/ && cd ${prot}/PsiPred/ ;\
$psipredplus ${prot}.fasta;'
```
Let's run now Disopred for this protein example:
```
docker run \
-v ${PsipredProtDB_PATH}:/home/database/ \
-e ${PsipredProtDB_NAME}=${uniref_fastafile} \
-v ${outputFolder}:/output \
-v ${inputFolder}:/input \
-e prot=$prot \
-e RunNumOfThreads=$CPUnum \
-it psipred_disopred_cpu:latest \
bash -c '\
mkdir -p ${prot}; \
mkdir -p ${prot}/DisoPred; \
cp /input/${prot}.fasta /output/${prot}/DisoPred/ && cd ${prot}/DisoPred/ ;\
$disopredplus ${prot}.fasta;'
```

Now let's see the predictions. The output files must have been saved here:

```
../CrossSpeciesWorkflow$ ls -l test/output/1pazA/PsiPred/
total 996
-rw-r--r-- 1 root root    131 Jun 11 14:36 1pazA.fasta
-rw-r--r-- 1 root root    612 Jun 11 14:37 1pazA.horiz
-rw-r--r-- 1 root root   3813 Jun 11 14:37 1pazA.ss
-rw-r--r-- 1 root root   3847 Jun 11 14:37 1pazA.ss2
-rw-r--r-- 1 root root 812138 Jun 11 14:37 psitmp1411ac0300.blast
-rw-r--r-- 1 root root 159201 Jun 11 14:37 psitmp1411ac0300.chk
-rw-r--r-- 1 root root    131 Jun 11 14:36 psitmp1411ac0300.fasta
-rw-r--r-- 1 root root  20983 Jun 11 14:37 psitmp1411ac0300.mtx

../CrossSpeciesWorkflow$ ls -l test/output/1pazA/DisoPred/
total 788
-rw-r--r-- 1 root root 124094 Jun 11 14:38 1pazA_9_11ac0300.blast
-rw-r--r-- 1 root root 159375 Jun 11 14:38 1pazA_9_11ac0300.chk
-rw-r--r-- 1 root root  21281 Jun 11 14:38 1pazA_9_11ac0300.mtx
-rw-r--r-- 1 root root     44 Jun 11 14:38 1pazA_9_11ac0300.pn
-rw-r--r-- 1 root root     35 Jun 11 14:38 1pazA_9_11ac0300.sn
-rw-r--r-- 1 root root   1987 Jun 11 14:39 1pazA.diso
-rw-r--r-- 1 root root   3507 Jun 11 14:38 1pazA.diso2
-rw-r--r-- 1 root root   2214 Jun 11 14:39 1pazA.dnb
-rw-r--r-- 1 root root    131 Jun 11 14:38 1pazA.fasta
-rw-r--r-- 1 root root    823 Jun 11 14:38 1pazA.horiz_d
-rw-r--r-- 1 root root 453217 Jun 11 14:39 1pazA.in_svm_dat
-rw-r--r-- 1 root root   1845 Jun 11 14:38 1pazA.nndiso
-rw-r--r-- 1 root root   2123 Jun 11 14:39 1pazA.out_svm_dat
-rw-r--r-- 1 root root   2156 Jun 11 14:39 1pazA.pbdat
```

<br /><br />

### A4. [SPOT-1D predictors](https://sparks-lab.org/server/spot-1d/) - from Sparks Lab  
SPOT-1D [\[HZ 2019\]](#hz-2019) is the updated version of Spider3 containing also additional features such as :
....

There are 2 available dokerfiles:
* CPU based
* GPU based

:exclamation: On progress


<br /><br />  
    
## B. Glycosylation module
  
### B1. Glycosylation predictors - from DTU Health Tech 

The [DTUHealthTech_Glycosylation_CPU Dockerfile](CrossSpeciesWorkflow/Dockerfiles/Glycosylation/DTUHealthTech_Glycosylation_CPU.Dockerfile) contains installation instructions for the following predictors from DTU Health Tech :
* [NetNGlyc v1.0](https://services.healthtech.dtu.dk/service.php?NetNGlyc-1.0) predicts N-Glycosylation sites in human proteins [\[GJB 2004\]](#gjb-2004). [CLI user guide](http://www.cbs.dtu.dk/cgi-bin/nph-runsafe?man=netNglyc)
    
* [NetOGlyc v4.0](https://services.healthtech.dtu.dk/service.php?NetOGlyc-4.0) predicts O-GalNAc (mucin type) glycosylation sites in mammalian proteins. [\[SC 2013\]](#sc-2013):
    
* [YinOYang v1.2](https://services.healthtech.dtu.dk/service.php?YinOYang-1.2) predicts O-(beta)-GlcNAc glycosylation and Yin-Yang sites [\[GB 2002\]](#gb-2002), [\[G 2001\]](#g-2001). 
Also includes SignalP and NetPhos v3.1 predictors (discussed in their corresponding module).
    
* [NetCGlyc v1.0](http://www.cbs.dtu.dk/services/NetCGlyc/) predicts C-mannosylation sites in mammalian proteins [\[J 2007\]](#j-2007).


As all DTU predictors license is for academic and non-profit usage only, in order to download the software it is required to register on their website and accept the license agreement prior accessing the download page. 

Please register and download the above predictors (linux version as the dockerfile image is ubuntu based) from the [Download link](https://services.healthtech.dtu.dk/software.php)

After you complete the license agreement and download the software, you can proceed building the docker image:




## C. Phosphorylation module :  

### C1. Phosphorylation predictors - from DTU Health Tech 

The [DTUHealthTech_Phosphorylation_CPU Dockerfile](CrossSpeciesWorkflow/Dockerfiles/Phosphorylation/DTUHealthTech_Phosphorylation_CPU.Dockerfile) contains installation instructions for the following predictors from DTU Health Tech :
* [NetPhos v3.1](https://services.healthtech.dtu.dk/service.php?NetPhos-3.1) predicts serine, threonine or tyrosine phosphorylation sites in eukaryotic proteins, either generic or kinase specific (17 kinases) [\[BGB 1999\]](#bgb-1999), [\[BB 2004\]](#bb-2004).
* [NetPhospan v1.0](https://services.healthtech.dtu.dk/service.php?NetPhospan-1.0) predicts phophorylation sites from a set of 120 human kinase [\[FN 2018\]](#fn-2018).


As all DTU predictors license is for academic and non-profit usage only, in order to download the software it is required to register on their website and accept the license agreement prior accessing the download page. 

Please register and download the above predictors (linux version as the dockerfile image is ubuntu based) from the [Download link](https://services.healthtech.dtu.dk/software.php)

After you complete the license agreement and download the software, you can proceed building the docker image:
```
cd ${CSW_HOME}/dockerfiles/phosphorylation/dtu_predictors

cp ${netphospan_SOURCE}/netphospan-1.0* ${CSW_HOME}/dockerfiles/phosphorylation/dtu_predictors/
cp ${netphospan_SOURCE}/netphospan-1.0* ${CSW_HOME}/dockerfiles/phosphorylation/dtu_predictors/

docker build -t dtu_phosphorylation_cpu -f dtu_phosphorylation_cpu.dockerfile .    
```

<br /><br />

### C2. [MusiteDeep Phosphorylation predictors](https://www.musite.net/) 

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


# CWL pipelines
:exclamation: On progress

## Structural prediction only

## PTS predictions

## All available predictors



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




