# Cross Species Structural, Post translational modifications and Functional protein predictions workflow

Content summary:
* [General Info](#general-info)
* [Project status](#project-status)
* [Installation](#installation)
* [Modules](#modules)
* [Usage](#usage)

## General Info
This repo intends to create an easy, user accesible and open-source tool for running a series of third party predictions software. The main focus is on:
* Dockerfiles for easy installing existing prediction software.
* a Python API for facilitating parsing and organising each predictor's output data.
* a common workflow language (CWL) pipeline that facilitates large protein sequences sets prediction jobs submissions.  

## Project status 
The project is currently under development. Currently there are 3 main modules that deal with:
* Structural related predictors (secondary structure, relative solvent accesibility and intrinsical disorder regions predictions)
* Glycosylaytion predictors
* Phosphorylation

## Installation

The setup has the following steps:

### Install prerequisites:

Docker client: 
	* Docker Desktop for Windows or MAC - [click](https://www.docker.com/products/docker-desktop)
	* docker-ce-cli for Linux - [click](docs.docker.com/install/linux/docker-ce/ubuntu/)

Cwltool - [click](https://github.com/common-workflow-language/cwltool)
Python3


### Clone repo
```
    git clone https://github.com/eliza-m/CrossSpeciesWorkflow.git
```

### Create docker images of the modules or individual predictors you are interested in. 

Please note that some of the predictors require registering on their website in order to download the source code. Also make sure that you have enough disk space available at the location were the docker image is being stored. Details of each predictors are shown bellow

### Modules

### A. Structural module

#### A1. RaptorX Protein Structure Property Prediction - from Xu group

Links:
* [Website](http://raptorx.uchicago.edu/StructurePropertyPred/predict/)
* [Github repo & manual](https://github.com/realbigws/Predict_Property) 


Docker image contains:
* Secondary structure (SS) predictions (SS3 & SS8 - 3 and 8 classes classification) [\[WLLX 2016\]](#wllx-2016), [\[WPMX 2016\]](#wpmx-2016), [\[WSX 2016\]](#wsx-2016)
* Relative solvent accesibility (RSA) 
* Disorder prediction - AUCpreD [\[WMX 2016\]](#wmx-2016), [\[WSX 2016\]](#wsx-2016)
* Transmembrane topology - TopoPred (TM2 & TM8 - 2 and 8 classes classification) [\[WG 2019\]](#wg-2019)


Build docker image
```
	sudo docker ...
```

Get protein sequence database, according to the sequence profile generator sofware you want to use (installed in the docker image): 

* HHblits (default):
    *  UniProt20 (default) :
    http://wwwuser.gwdg.de/~compbiol/data/hhsuite/databases/hhsuite_dbs/old-releases/uniprot20_2016_02.tgz
    *  UniClust30 :
    http://wwwuser.gwdg.de/~compbiol/uniclust/2017_10/uniclust30_2017_10_hhsuite.tar.gz
    
* jackhmm :
    * uniref50 :
    ftp://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref50/uniref50.fasta.gz
    * uniref90 :
    ftp://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref90/uniref90.fasta.gz
  
* buildali2 :
    This should be mounted (or using simlinks) in "databases/nr_databases" (must contain nr90 and nr70).
    http://raptorx.uchicago.edu/download/
    


#### A2. SCRATCH-1D Protein Predictor v1.2 & DisPRO1.0 - from Baldi group  

Links:
* [Website](http://scratch.proteomics.ics.uci.edu/)
* [Documentation](http://download.igb.uci.edu/SCRATCH-1D_documentation.txt; 
* [Installation guide](http://download.igb.uci.edu/SCRATCH-1D_readme.txt) 

Docker image contains 2 packages:
* SCRATCH-1D v1.2 [\[MB 2014\]](#mb-2014), [\[CRSB 2005\]](#crsb-2005) :
    * Secondary structure predictions (SSpro3 & SSpro8 - 3 and 8 classes classification) 
    * Relative solvent accesibility (ACCpro).
* DISpro1.0 Disorder prediction [\[CSB 2005\]](#csb-2005) 


### B. Glycosylation module

#### B1. Glycosylation predictors - from DTU Health Tech 

Docker image contains the following predictors:
* [NetNGlyc v1.0](https://services.healthtech.dtu.dk/service.php?NetNGlyc-1.0) 
Predicts N-Glycosylation sites in human proteins [\[GJB 2004\]](#gjb-2004). 
[CLI user guide](http://www.cbs.dtu.dk/cgi-bin/nph-runsafe?man=netNglyc)
    
* NetOGlyc v4.0 (https://services.healthtech.dtu.dk/service.php?NetOGlyc-4.0)
Predicts O-GalNAc (mucin type) glycosylation sites in mammalian proteins. [\[SC 2013\]](#sc-2013):
    
* [YinOYang v1.2](https://services.healthtech.dtu.dk/service.php?YinOYang-1.2)
Predicts O-(beta)-GlcNAc glycosylation and Yin-Yang sites [\[GB 2002\]](#gb-2002), [\[G 2001\]](#g-2001). 
Also includes SignalP and NetPhos v3.1 predictors (discussed in their corresponding module).
    
* [NetCGlyc v1.0](http://www.cbs.dtu.dk/services/NetCGlyc/)
Predicts C-mannosylation sites in mammalian proteins [\[J 2007\]](#j-2007).








As all DTU predictors require to register using an academic account prior accesing the download page, we could not integrate and automatise the download step into the pipeline.

Please register and download the above predictors (linux version as the docker image is ubuntu based) from the link bellow:

[Download link](https://services.healthtech.dtu.dk/software.php)

Afterwards, you can proceed building the docker image:
```
	sudo ...
```



### C. Phosphorylation module :

#### C1. Phosphorylation predictors - from DTU Health Tech 
NetPhos
NetPhospan
YinOYang

https://services.healthtech.dtu.dk/service.php?NetPhos-3.1

Sequence- and structure-based prediction of eukaryotic protein phosphorylation sites.
Blom, N., Gammeltoft, S., and Brunak, S.
Journal of Molecular Biology: 294(5): 1351-1362, 1999.

Prediction of post-translational glycosylation and phosphorylation of proteins from the amino acid sequence.
Blom N, Sicheritz-Ponten T, Gupta R, Gammeltoft S, Brunak S.
Proteomics: Jun;4(6):1633-49, review 2004.


https://services.healthtech.dtu.dk/service.php?NetPhospan-1.0

A generic Deep Convolutional Neural Network framework for prediction of Receptor-ligand Interactions. NetPhosPan; Application to Kinase Phosphorylation prediction.
Emilio Fenoy, Jose M. G. Izarzugaza, Vanessa Jurtz, Søren Brunak and Morten Nielsen.
Bioinformatics (2018).



## Usage

## References

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




