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

### Structural module

#### 1. RaptorX-Property [\[WLLX 2016\]](#wllx-2016)

* 
* 

RaptorX-property 
Scratch
Spot-1D (Spider3)
I-tasser
PsiPred

Disopred

#### Glycosylation predictors:

NetNGlyc.
[User guide](http://www.cbs.dtu.dk/cgi-bin/nph-runsafe?man=netNglyc)
[Download upon registering](https://services.healthtech.dtu.dk/software.php)

NetOGlyc

NetCGlyc

#### Phosphorylation predictors:
NetPhos
NetPhospan
YinOYang





## Usage

## References

##### \[WLLX 2016\]

Wang, S.; Li, W.; Liu, S.; Xu, J. RaptorX-Property: a web server for protein structure property prediction. Nucleic Acids Res. 2016, 44, W430–W435.

Wang, S.; Peng, J.; Ma, J.; Xu, J. Protein Secondary Structure Prediction Using Deep Convolutional Neural Fields. Sci. Rep. 2016, 6, 1–11.

Wang, S.; Ma, J.; Xu, J. AUCpreD: Proteome-level protein disorder prediction by AUC-maximized deep convolutional neural fields. In Proceedings of the Bioinformatics; Oxford University Press, 2016; Vol. 32, pp. i672–i679.

Wang, S.; Sun, S.; Xu, J. AUC-maximized deep convolutional neural fields for protein sequence labeling. In Proceedings of the Lecture Notes in Computer Science (including subseries Lecture Notes in Artificial Intelligence and Lecture Notes in Bioinformatics); Springer Verlag, 2016; Vol. 9852 LNAI, pp. 1–16.
					
Remmert, M.; Biegert, A.; Hauser, A.; Söding, J. HHblits: Lightning-fast iterative protein sequence searching by HMM-HMM alignment. Nat. Methods 2012, 9, 173–175.
