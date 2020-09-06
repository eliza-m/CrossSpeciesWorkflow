# Cross Species Structural, Post translational modifications and Functional protein predictions workflow

Content summary:
* [General Info](#general-info)
* [Installation and Setup](#installation-and-setup)
* [Running CWL workflows](#running-cwl-workflows)
* [Prediction Modules Description](#prediction-modules-description)
* [Python API](#python-api)
* [Known issues](#known-issues)
* [References](#references)


# General Info

This project is a scalable workflow that receives either the protein FASTA file or a list of Uniprot IDs and runs a series of structural and phenotype related predictors, generating a knowledge dataset that will facilitate further exploration and comparisons according to the following categories of features: secondary structure, solvent accessibility, disordered regions, PTS modifications (phosphorylation, glycosylation, lipid modification, sumoylation, etc).

Currently there are 7 main modules that deal with different types of predictions :
* A. Structural related
* B. Phosphorylation
* C. Glycosylaytion 
* D. Acetylation 
* E. Sumoylation 
* F. Lipid modification
* G. Cellular localisation

This repo intends to create an easy, user accesible and open-source tool for running a series of third party predictions software. Provided are :
* Dockerfiles for easy installing existing prediction software.
* Python API for facilitating parsing and organising each predictor's output data.
* CWL pipelines that facilitates large protein sequences sets prediction jobs submissions and parallelisation.  


### Project status 
The project is under active development and it was tested so far only on native Ubuntu 18 & 20 .

<br />  

# Installation and Setup

## Requirements before using CrossSpeciesWorkflow: 
To run CWL workflows you can use any CWL runner of your choice. By default (and also for the ease of debugging) we used [CWLtool](github.com/common-workflow-language/cwltool) [\[AC 2017\]](#ac-2017).

#### Install Prerequisites
* Docker client: 
    * Docker Desktop for Windows or MAC - [click](https://www.docker.com/products/docker-desktop)
    * docker-ce-cli for Linux - [click](docs.docker.com/install/linux/docker-ce/ubuntu/)
* cwltool - [click](https://github.com/common-workflow-language/cwltool). It can be either downloaded or the user can just use the python environment.
* Python3.8 and above (Optional: for separately using the Python API outisde the CWL pipeline)


## Clone repo
```
$ git clone https://github.com/eliza-m/CrossSpeciesWorkflow.git
$ git checkout GSOC2020
```
Please set the CrossSpeciesWorkflow project home variable and add it to `.bashrc` :
```
$ export CSW_HOME=/path/to/CrossSpeciesWorkflow/project/home
$ cd CSW_HOME
```
Conda environment that has cwltool and python is also provided.
```bash
$ conda env create -f environment.yaml
```
The python code in this project is published as a conda package.
```bash
$ conda activate species_proteins
$ python setup.py install
```

## Setup sequence databases

This step **can be skipped** if you do not intend to use the **Structural module**.
Only the structural predictors require downloading and setting up different protein databases. Links for download are provided bellow
* RaptorX
    * Uniprot20 : http://wwwuser.gwdg.de/~compbiol/data/hhsuite/databases/hhsuite_dbs/old-releases/uniprot20_2016_02.tgz
* Psipred & Disopred:
    * UniRef50/UniRef90 FASTA format : http://uniprot.org/downloads. 

Afterwards, for UniRef50/UniRef90 a blast database needs to be created (these steps need to be done only once, afterwards the database can be used or moved anywhere):
```bash
# if you do not habe BLAST+ installed run:
$ sudo apt-get install ncbi-blast+
	
# go to the place where Uniref fasta file is being stored (change the path bellow accordingly):
$ cd /Place/where/UnirefX.fasta/file/is/stored
	
# create database (this might take a while from several minutes to one hour)
$ makeblastdb -dbtype prot -in uniref50.fasta
```
For easing the CWL pipeline submission, please create symbolic links with the downloaded & prepared databases:
```
$ ln -s /path/to/host/db/folder/uniprot20_2016_02 ${CWL_HOME}/databases/uniprot20_2016_02
$ ln -s /path/to/host/db/folder/uniref50 ${CWL_HOME}/databases/uniref50
```
The setup databases should contain:
```
$ ls ${CSW_HOME}/databases/uniprot20_2016_02
md5sum                          uniprot20_2016_02.cs219          uniprot20_2016_02_hhm_db.index
uniprot20_2016_02_a3m_db.index  uniprot20_2016_02_cs219.ffdata   uniprot20_2016_02_hhm.ffdata
uniprot20_2016_02_a3m.ffdata    uniprot20_2016_02_cs219.ffindex  uniprot20_2016_02_hhm.ffindex
uniprot20_2016_02_a3m.ffindex   uniprot20_2016_02.cs219.sizes

$ ls ${CSW_HOME}/databases/uniref50
uniref50.fasta         uniref50.fasta.02.pin  uniref50.fasta.05.phr  uniref50.fasta.07.psq
uniref50.fasta.00.phr  uniref50.fasta.02.psq  uniref50.fasta.05.pin  uniref50.fasta.08.phr
uniref50.fasta.00.pin  uniref50.fasta.03.phr  uniref50.fasta.05.psq  uniref50.fasta.08.pin
uniref50.fasta.00.psq  uniref50.fasta.03.pin  uniref50.fasta.06.phr  uniref50.fasta.08.psq
uniref50.fasta.01.phr  uniref50.fasta.03.psq  uniref50.fasta.06.pin  uniref50.fasta.pal
uniref50.fasta.01.pin  uniref50.fasta.04.phr  uniref50.fasta.06.psq  uniref50.release_note.txt
uniref50.fasta.01.psq  uniref50.fasta.04.pin  uniref50.fasta.07.phr
uniref50.fasta.02.phr  uniref50.fasta.04.psq  uniref50.fasta.07.pin
```

<br />  

# Running CWL workflows #

### Intro

[CWL](https://www.commonwl.org/) workflow scripts provide a easy on-step way to run a series of multi step operations in a scalable and parallelised fashion. Running such a workflow requires: 

* a workflow manager (we use [cwltool](https://github.com/common-workflow-language/cwltool))
* a cwl script (found in `${CSW_HOME}/cwl` directory) that defines the workflow procedure, paramaters and how inputs and outputs of different steps relate to each other. These are scripts **do not need editing** when using different input data or parameters.
* input file - YML or JSON (examples can be found in `${CSW_HOME}/tests/cwl/test_modules/`) that define where the input files are, values of mandatory / optional parameters.


### CWL workflow scripts

The CWL workflow scripts are provided `in ${CSW_HOME}/cwl` directory, for each prediction type module, but also for an overall pipeline covering all modules.

Individual modules short names are :
* **struct** - Structural related
* **phos**   - Phosphorylation
* **glyc**   - Glycosylaytion 
* **acet**   - Acetylation 
* **sumo**   - Sumoylation 
* **loc**    - Cellular localisation
* **lipid**  -Lipid modification

While the following refer to **grouped** predictions modules :
* **ptm** - All Post Translation Modification modules (acet + glyc + phos + sumo + lipid)
* **all** - All modules

Specific modules can be run individually using designated CWL workflow scripts found in their corresponding modules folder.
Provided are tools for different input types such as:

* **single protein FASTA**    : 1prot_$module_only_fasta.cwl
* **single protein ID**       : 1prot_$module_only_id.cwl
* **multi protein ID array**  : Nprot_$module_only_id.cwl

**The disctinction between single & multi protein mode is that in multi protein mode, sequences are aligned using Clustal Omega in the final output layout.**  

Example YML input files are provided within `${CSW_HOME}/tests/cwl/test_modules/` for each input type (single protein FASTA or ID or a list of IDs).

Usage example for a specific module only for a list of protein IDs would be :
```
### INDIVIDUAL MODULES
# Structural
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/structural/Nprot_struct_only_id.cwl [YML/JSON file]

# Acetylation
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/acetylation/Nprot_acet_only_id.cwl [YML/JSON file]

# Glycosylation
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/glycosylation/Nprot_glyc_only_id.cwl [YML/JSON file]

# Phosphorylation
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/phosphorylation/Nprot_phos_only_id.cwl [YML/JSONfile]

# Lipid modification
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/lipid/Nprot_lipid_only_id.cwl [YML/JSON file]

# Sumoylation 
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/sumoylation/Nprot_sumo_only_id.cwl [YML/JSON file]

# Localisation
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/localisation/Nprot_loc_only_id.cwl [YML/JSON file]

### GROUPED MODULES
# PTM predictions
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/Nprot_ptm_id.cwl [YML/JSON file]

# ALL
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/Nprot_all_id.cwl [YML/JSON file]
```

### Testing CWL workflows

All tests can be run simultaneously by running `${CSW_HOME}/tests/cwl/test_modules/test_all_module.sh`. 
Output samples for each cwl workflow are found in in module folder in `expected_ourput` directories.

```
$ cd ${CSW_HOME}/tests/cwl/test_modules/
$ bash test_all_module.sh
```


### Output files

Current outputs are module based and consists of:
* a directory containing all raw predictions outputs named `$protname_$module_preds`
* a summary file in `tsv` format named `$module_results.tsv` that contains all predictions output parsed and organised in a comparative manner.

A HTML/JSON output format is currently under development.

The summary tsv file for **single protein format** has a 3-row header. 
First 2 columns contain **resids** and **amino acids**.
Next columns (3 to end) contain predictions ouput. the subheaders refer to :
* 1st - prediction method name
* 2nd - prediction type (such as STY-phosphorylation, Nter-acetylation, K-acetylation)
* 3rd - predictor specific details or conditions (such as a particular enzyme, or number of classes the prediction refers to). These are predictor specific, so the user needs to be aquinted with each individual prediction methods particularities and how data should be interpreted.

Example - acetylation module :
```
resid	aa	netacet	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	
 	 	N-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	
 	 	 	CREBBP	EP300	HAT1	KAT2A	KAT2B	KAT5	KAT8	
1	M	-	-	-	-	-	-	-	-	
2	T	0.482	-	-	-	-	-	-	-	
3	E	-	-	-	-	-	-	-	-	
4	Q	-	-	-	-	-	-	-	-	
5	M	-	-	-	-	-	-	-	-
...
```


The summary tsv file for **multi protein format** has a 4-row header. 
First column contain **alignment numbering** 
Next N columns contain **amino acids** of the N sequences predicted.
Column N+2 named 'Dif' shows positions where sequence differences exist in alignment (marked with * symbol).
Next columns (from N+3 to end) contain predictions ouput. the subheaders refer to :
* 1st - predictor method name
* 2nd - prediction type (such as STY-phosphorylation, Nter-acetylation, K-acetylation)
* 3rd - predictor specific details or conditions (such as a particular enzyme, or number of classes the prediction refers to). These are predictor specific, so the user needs to be aquinted with each individual prediction methods particularities and how data should be interpreted.
* 4th - Protname / ProtID to which the prediction refers to.

Example - acetylation module:

```
alnid	P63244	O42248	O18640	P38011	Dif	netacet	netacet	netacet	netacet	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	gpspail	
 	 	 	 	 	 	N-acet	N-acet	N-acet	N-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	K-acet	
 	 	 	 	 	 	 	 	 	 	CREBBP	CREBBP	CREBBP	CREBBP	EP300	EP300	EP300	EP300	HAT1	HAT1	HAT1	HAT1	KAT2A	KAT2A	KAT2A	KAT2A	KAT2B	KAT2B	KAT2B	KAT2B	KAT5	KAT5	KAT5	KAT5	KAT8	KAT8	KAT8	KAT8	
 	 	 	 	 	 	P63244	O42248	O18640	P38011	P63244	O42248	O18640	P38011	P63244	O42248	O18640	P38011	P63244	O42248	O18640	P38011	P63244	O42248	O18640	P38011	P63244	O42248	O18640	P38011	P63244	O42248	O18640	P38011	P63244	O42248	O18640	P38011	
1	-	-	-	M	*	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	
2	-	-	-	A	*	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	
3	M	M	M	S	*	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	
4	T	T	S	N	*	0.482	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	
5	E	E	E	E		-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	-	
```



Example - structural module:

```
alnid	P63244	O42248	O18640	P38011	Dif	raptorx	raptorx	raptorx	raptorx	psipred	psipred	psipred	psipred	raptorx	raptorx	raptorx	raptorx	raptorx	raptorx	raptorx	raptorx	raptorx	raptorx	raptorx	raptorx	disopred	disopred	disopred	disopred	
 	 	 	 	 	 	SS	SS	SS	SS	SS	SS	SS	SS	SS	SS	SS	SS	ACC	ACC	ACC	ACC	DIS	DIS	DIS	DIS	DIS	DIS	DIS	DIS	
 	 	 	 	 	 	3-class	3-class	3-class	3-class	3-class	3-class	3-class	3-class	8-class	8-class	8-class	8-class	3-class	3-class	3-class	3-class	2-class	2-class	2-class	2-class	2-class	2-class	2-class	2-class	
 	 	 	 	 	 	P63244	O42248	O18640	P38011	P63244	O42248	O18640	P38011	P63244	O42248	O18640	P38011	P63244	O42248	O18640	P38011	P63244	O42248	O18640	P38011	P63244	O42248	O18640	P38011	
1	-	-	-	M	*	C	C	C	C	C	C	C	C	C	C	C	C	E	E	E	E	D	D	D	D	-	-	-	D	
2	-	-	-	A	*	C	C	C	C	C	C	C	C	C	C	C	C	E	E	E	E	D	D	D	D	-	-	-	D	
3	M	M	M	S	*	C	C	C	C	C	C	C	C	C	C	C	C	E	E	E	E	D	D	D	D	D	D	D	D	
4	T	T	S	N	*	C	C	C	C	C	C	C	C	C	C	C	C	E	E	E	E	D	D	D	D	-	-	-	-	
5	E	E	E	E		C	C	C	C	C	C	C	C	C	C	C	C	E	E	E	E	D	D	D	-	-	-	-	-	
6	Q	Q	T	V	*	E	C	C	E	C	C	C	C	E	C	C	E	E	E	E	M	-	D	-	-	-	-	-	-	
7	M	M	L	L	*	E	E	E	E	E	E	C	E	E	E	E	E	M	M	M	M	-	-	-	-	-	-	-	-	
...
```


<br />


## Prediction Modules Description

### A. Structural module  

#### A1. [RaptorX Protein Structure Property Prediction](http://raptorx.uchicago.edu/StructurePropertyPred/predict/) - from Xu group

The [RaptorX-Property repo](https://github.com/realbigws/RaptorX_Property_Fast) linked to the journal paper has been upgraded and split into 2 packages: 
* [Predict_Property - github repo & manual](https://github.com/realbigws/Predict_Property) 
* [TGT Package - github repo & manual](https://github.com/realbigws/TGT_Package)

Predictions methods included: 
* Secondary structure (SS) predictions (SS3 & SS8 - 3 and 8 classes classification) [\[WLLX 2016\]](#wllx-2016), [\[WPMX 2016\]](#wpmx-2016), [\[WSX 2016\]](#wsx-2016)
* Relative solvent accesibility (RSA) 3 class classification 
* Disorder prediction - AUCpreD [\[WMX 2016\]](#wmx-2016), [\[WSX 2016\]](#wsx-2016)


#### A2. [Psipred](http://bioinf.cs.ucl.ac.uk/psipred/) - from UCL Bioinformatics group  

Docker image contains PSIPRED Protein Secondary Structure Predictor v4.0 ([github repo](https://github.com/psipred/psipred)) [\[BJ 2019\]](#bj-2019), [\[J 1999\]](#j-1999).

Predicts secondary structure (SS) predictions - 3 class prediction

#### A3. [Disopred](http://bioinf.cs.ucl.ac.uk/psipred/) - from UCL Bioinformatics group  
Docker image contains DISOPRED Disorder Predictor v3.1 ([github repo](https://github.com/psipred/disopred)) [\[JC 2014\]](#jc-2014)

Predicts intrinsically disordered regions - 2 class prediction

<br />  

### B. Phosphorylation module

#### B1. [NetPhos v3.1](https://services.healthtech.dtu.dk/service.php?NetPhos-3.1) 

Predicts serine, threonine or tyrosine phosphorylation sites in eukaryotic proteins, either generic or kinase specific (17 kinases) [\[BGB 1999\]](#bgb-1999), [\[BB 2004\]](#bb-2004).
We integrated in the main worklow only the online submission mode.
However, also provided are a Dockerfile, as well python parsers and cwl tools to run NetPhos locally. Please see `CONTAINERS.md` for details and examples.

#### B2. [NetPhospan v1.0](https://services.healthtech.dtu.dk/service.php?NetPhospan-1.0) 

Predicts phophorylation sites from a set of 120 human kinase [\[FN 2018\]](#fn-2018).
We integrated in the main worklow only the online submission mode with generic type mode, due to the large number of available kinases models.
However, also provided are a Dockerfile, as well python parsers and cwl tools to run NetPhosPan locally. Please see `CONTAINERS.md` for details and examples.

#### B3. [MusiteDeep Phosphorylation predictors](https://www.musite.net/) 

MusiteDeep Phosphorylation ([github repo](https://github.com/duolinwang/MusiteDeep)) predicts general and/or kinase specific phosphorylation sites [\[WX 2017\]](#wx-2017). 

There are 2 available dokerfiles:
* MusiteDeep using Keras1 and Theano CPU-based
* MusiteDeep using Keras2 and Tensorflow CPU-based - which is much faster than Theano's version (used in CWL wf)

Predicts phophorylation sites at S/T/Y residues, in both generic or kinases specific mode (only for 'CDK','PKA','CK2', 'MAPK', 'PKC' kinases). Additionally it provides some custom models and the possibility to train custom models based on users data. Please see their documentation for detailed usage info.

Integrated in the main workflow are currently only generic type predictions at S, T and Y residues.

<br /> 

### C. Glycosylation module
  
#### C1. [NetNGlyc v1.0](https://services.healthtech.dtu.dk/service.php?NetNGlyc-1.0) 
Predicts N-Glycosylation sites in human proteins [\[GJB 2004\]](#gjb-2004). [CLI user guide](http://www.cbs.dtu.dk/cgi-bin/nph-runsafe?man=netNglyc)

#### C2. [NGlyDE](http://bioapp.iis.sinica.edu.tw/Nglyde/introduce.html) 
Predicts N-Glycosylation sites [\[PS 2019\]](#ps-2019).

#### C3. [NetOGlyc v4.0](https://services.healthtech.dtu.dk/service.php?NetOGlyc-4.0) 
Predicts O-GalNAc (mucin type) glycosylation sites in mammalian proteins. [\[SC 2013\]](#sc-2013):

#### C4. [ISOGlyP](https://isoglyp.utep.edu/) 
Predicts isoform specific mucin-type o-glycosylation sites [\[ML 2020\]](#ml-2020).
Github repo - https://github.com/jonmohl/ISOGlyP

#### C5. [NetCGlyc v1.0](http://www.cbs.dtu.dk/services/NetCGlyc/) 
Predicts tryptophan C-mannosylation sites in mammalian proteins [\[J 2007\]](#j-2007).

#### C6. [GlycoMine](http://glycomine.erc.monash.edu/Lab/GlycoMine/) 
Predicts C-, N- and O-linked glycosylation sites. [\[LS 2015\]](#ls-2015).

Only for ISOGlyP, the main workflow uses the docker images, while the rest of the predictions are submitted online.
However, for NetNGlyc, NetCGlyc and NetOGlyc, also provided are a Dockerfile, as well python parsers and cwl tools to run them locally. Please see `CONTAINERS.md` for details and examples.


<br />

### D. Acetylation module  

#### D1. [NetAcet v1.0](https://services.healthtech.dtu.dk/service.php?NetAcet-1.0) 
Predicts substrates Nε-lysine acetylation sites. [\[KB 2005\]](#kb-2005). 

#### D2. [GPSpail](http://pail.biocuckoo.org/) 
Predicts N-Glycosylation sites [\[DX 2016\]](#dx-2016).

Only online submitted predictions are currently available in the main workflow

<br />

### E. Sumoylation module  

#### E1. [SUMOgo](http://predictor.nchu.edu.tw/SUMOgo/) 
Predicts sumoylation (SUMO) lysine sites. [\[CC 2018\]](#cc-2018). 

#### E2. [GPSpail](http://sumosp.biocuckoo.org/) 
Predicts sumoylation sites (SUMO) and SUMO-interaction Motifs (SIM) [\[ZR 2014\]](#zr-2014).

Only online submitted predictions are currently available in the main workflow

<br />

#### F. Lipid modification module 

#### F1. [GPSlipid](http://lipid.biocuckoo.org/) 
Predicts lipid modification sites [\[XR 2016\]](#xr-2016)

Included are specific lipif PTMs predictors refering to:
* N-Myristoylation
* S-Palmitoylation
* S-Farnesylation	
* S-Geranylgeranylation

Only online submitted predictions are currently available in the main workflow


<br />

### G. Cellular localisation module   

#### G1. [TMHMM v2.0](http://www.cbs.dtu.dk/services/TMHMM/) 
Predicts transmembrane helices and orientation [\[KS 2001\]](#ks-2001)

#### G2. [TMpred](https://embnet.vital-it.ch/software/TMPRED_form.html)
Predicts transmembrane helices and orientation [\[HS 1993\]](#hs-1993)

Only online submitted predictions are currently available in the main workflow
for TMHMM, also provided are a Dockerfile, as well python parsers and cwl tools to run them locally. Please see `CONTAINERS.md` for details and examples.

<br />


# Python API 

The Python API is used directly by the CWL workflow. While completely **optional**, users can find convenient to use the Python API directly for particular purposes, such as the ones described bellow.  

## Command-line options

### Quick & dirty pipeline run 

A simplist selection of the cwl tool can be performed directly from Python API. However it offers a very limited number of options, therefore we recommend using directly CWLtool or other workflow runner

```bash
# Full pipeline & one protein example
$ python species_proteins/workflow/run.py pipeline --cwlinput tests/cwl/test_modules/1prot_id.yml --mode single 
--module all --outdir [path/to/dir]  

# Acetylation module & multi protein example
$ python species_proteins/workflow/run.py pipeline --cwlinput tests/cwl/test_modules/Nprot_id.yml --mode multi 
--module acet --outdir [path/to/dir]             ``` 
```
For other options, see help menu:
```
$ python species_proteins/workflow/run.py pipeline --help
Usage: run.py pipeline [OPTIONS]

  Simple wrapper for choosing which CWL workflow to run. For more options
  uses directly cwltool or a different workflow runner.

Options:
  --cwlinput TEXT  YML or JSON input file with Uniprot IDs. See provided
                   examples in /tests folder  [required]

  --mode TEXT      "single" or "multi" protein analysis  [required]
  --module TEXT    Prediction module - accepted values:
                   - all            :  All modules
                   - ptm            :  All Post Translation modifications ( glyc + acet + phos + sumo + lipid)
                   - struct         :  Structural module
                   - glyc           :  Glycosylation module
                   - phos           :  Phosphorylation module
                   - acet           :  Acetylation module
                   - lipid          :  Lipid modification module
                   - sumo           :  Sumoylation module
                   - loc            :  Cellular localisation module   [required]

  --outdir TEXT    Output directory. Default: current directory.
  --args TEXT      Argumments to be passed to cwltool.  [default: --no-match-
                   user --no-read-only]

  --parallel       Run in parallel. NOT recommended due to HTTP response
                   errors !!!  [default: False]

  --help           Show this message and exit.
```


<br />

### Predictions merged output layout & and easy change between output layouts 

Let's assume that you have already performed an "all" module prediction pipeline for your proteins and you want to generate a formatted output only for a specific sequence and only for glycosylation related predictors.

```
$ python species_proteins/workflow/run.py format-output --format single --module glyc 
--inputfolder [path/to/predictions/dir] --protname YourID
```
As a input folder you can provide directly the overall prediction folder (that containes multiple proteins predictions) and the provided ID will be searched for (prediction output naming is $protID.predictor.*), but if you provide directly the folder of the desired protein the `--protname` argument is no longer needed.


For other options, see help menu:
```
$ python species_proteins/workflow/run.py format-output --h
elp
Usage: run.py format-output [OPTIONS]

  Generates a vertical formatted layout of all predicted outputs. If 'multi'
  protein format is selected, sequences are shown aligned.

Options:
  --format TEXT       "single" or "multi" protein layout  [required]
  --module TEXT       Prediction module - accepted values:
                      - all            :  All modules
                      - ptm            :  All Post Translation modifications ( glyc + acet + phos + sumo + lipid)
                      - struct         :  Structural module
                      - glyc           :  Glycosylation module
                      - phos           :  Phosphorylation module
                      - acet           :  Acetylation module
                      - lipid          :  Lipid modification module
                      - sumo           :  Sumoylation module
                      - loc            :  Cellular localisation module   [required]

  --inputfolder TEXT  Input folder where all prediction results are stored
                      [required]

  --output TEXT       Output formatted file  [required]
  --signif            Print only significant predicted sites. It applies only
                      for PTM predictors (significance thresholds are method
                      specific.)  [default: False]

  --protname TEXT     Only for single protein format, when within the specified input
                      folder there are multiple files with the same extension, a basename of the protein should be provided.
                      Example: protname.predictor.out; Default: null

  --alnfile TEXT      Required for "multi" protein layout.
  --help              Show this message and exit.
```


<br />

### Submit online jobs for a specific predictor on their own webserver.

Some of the predictors can be used only on their webserver. We provide a easy to use tool to directly submit a prediction job on predictor's webserver via POST & GET.

Usage example:
```
$ python species_proteins/workflow/run.py submit-online --input MyPROT.fasta --predictor gpslipid --output MyPROT.gpslipid.html 
```
Some online predictors accept multiFASTA input, some do not...

Other options:
```

$ python species_proteins/workflow/run.py submit-online --h
elp
Usage: run.py submit-online [OPTIONS]

  Submit online jobs for a given predictor

Options:
  --input TEXT      Input FASTA file   [required]
  --output TEXT     Output filename  [required]
  --predictor TEXT  Online predictor to submit sequence to. Predictors list per categories :
                    - Glycosilation: 'netcglyc', 'netnglyc', 'netoglyc', 'glycomine', 'nglyde'
                    - Acetylation: 'netacet', 'gpspail'
                    - Phosphorylation: 'netphos', 'netphospan'
                    - Lipid modification: 'gpslipid'
                    - Sumoylation: 'gpssumo', 'sumogo'
                    - Cellular localisation: 'tmhmm', 'tmpred'   [required]

  --type TEXT       Additional arguments to be passed; predictor specific
                    (glycomine: "N" or "C" or "O" glicosylation)

  --help            Show this message and exit.
```

IMPORTANT !!!:
Some online predictors forms do not handle well commonly used FASTA headers, therefore we recommend using as header directly the protein name (no spaces) or ID. Example: `>LEUK_RAT` or '>P12345'. 

Also, in order to easily use the provided parsers for each predictor, we recommend to use prediction output filenames that follow the rule $protname.$predictor.*
Examples: 'LEUK_RAT.netnglyc.html', 'P12345.nglyde.out', etc. 


To ease FASTA files retrieval and manipulation, you can use the provided `get-fasta` CLI function. An example of retrieving sequences of a protein ID and trimming the header youd be:
```
$ python species_proteins/workflow/run.py get-fasta --uniprot P12345 --trimheader
```

Other options
```
$ python species_proteins/workflow/run.py get-fasta --help
Usage: run.py get-fasta [OPTIONS]

  Retrieves fasta file from UniprotKB ID

Options:
  --uniprot TEXT   Uniprot ID to fetch  [required]
  --filename TEXT  Filename to save. Default $id.fasta
  --trimheader     Trimm header to contain only id  [default: False]
  --mode TEXT      Write("w") or append("a") mode  [default: w]
  --help           Show this message and exit.
```

#### Python API structure

Found in `${CSW_HOME}/species_proteins` the API is structured on a module basis. Each module folder contains: 
* Predictor classes `$predictor_data.py` that deal with input preparation, raw outputs parsing and, for a series of predictors, online job submission.
* Module classes `$module_pred.py` (inherit Module_pred base class) deal with :
    * raw output paths retrieval
    * organizing multiple predictors results
    * printing results in comparative layout.
    
<br />

# Known issues

CWL workflow related :
* some code duplication due to CWL v1.0 limitations. CWL v1.2 (currently under development) will support IF operator and we will address this when v1.2 becomes stable.
* The cwltool flags `--no-match-user` and `--no-read-only` are necessary due to permissions issues (because some of the predictors require generating or editing files in specific locations)

Output related:
* right now only `tsv` outputs are supported, html/json versions are in development.


<br />

# References 

Contains all reference found within the repo.

##### \[AC 2017\]
Amstutz, P, Crusoe, MR, Singh, M, Kumar, K, Chilton, J, [Unknown], B, Soiland-Reyes, S, Chapman, B, Kotliar, M, Leehr, D, Carrasco, G, Kartashov, A, Tijanic, N, Ménager, H, Safont, PR, Porter, JJ, Molenaar, G, Yuen, D, Barrera, A, Ivkovic, S, Spangler, R, [Unknown], P, Tanjo, T, Vandewege, W, Randall, JC, Kern, J, Bradley, J, Li, J, der Zwaan, JV & Connelly, A, common-workflow-language/cwltool, 2017, Software, GitHub, GitHub. <https://github.com/common-workflow-language/cwltool/releases/tag/1.0.20170828135420>


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


<br />

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


<br />

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
##### \[PS 2019]
Pitti T, Chen CT, Lin HN, Choong WK, Hsu WL, Sung TY. N-GlyDE: a two-stage N-linked glycosylation site prediction incorporating gapped dipeptides and pattern-based encoding. Sci Rep. 2019;9(1):15975. Published 2019 Nov 4. doi:10.1038/s41598-019-52341-z
##### \[LS 2015]
Li F, Li C, Wang M, Webb GI, Zhang Y, Whisstock JC, Song J. GlycoMine: a machine learning-based approach for predicting N-, C-and O-linked glycosylation in the human proteome. Bioinformatics, 2015, 31(9):1411-1419. doi:10.1093/bioinformatics/btu852


<br />

### Acetylation predictors:
##### \[KB 2005]
Kiemer L, Bendtsen JD, Blom N. NetAcet: prediction of N-terminal acetylation sites. Bioinformatics. 2005;21(7):1269-1270. doi:10.1093/bioinformatics/bti130
##### \[DX 2016]
Deng W, Wang C, Zhang Y, et al. GPS-PAIL: prediction of lysine acetyltransferase-specific modification sites from protein sequences. Sci Rep. 2016;6:39787. Published 2016 Dec 22. doi:10.1038/srep39787
<br /><br />

### Sumoylation predictors:
##### \[CC 2018]
Chang, C., Tung, C., Chen, C. et al. SUMOgo: Prediction of sumoylation sites on lysines by motif screening models and the effects of various post-translational modifications. Sci Rep 8, 15512 (2018). https://doi.org/10.1038/s41598-018-33951-5
##### \[ZR 2014]
Zhao Q, Xie Y, Zheng Y, et al. GPS-SUMO: a tool for the prediction of sumoylation sites and SUMO-interaction motifs. Nucleic Acids Res. 2014;42(Web Server issue):W325-W330. doi:10.1093/nar/gku383

<br />

### Lipid modification predictors:
##### \[XR 2016]
Xie Y, Zheng Y, Li H, et al. GPS-Lipid: a robust tool for the prediction of multiple lipid modification sites. Sci Rep. 2016;6:28249. Published 2016 Jun 16. doi:10.1038/srep28249

<br />

### Celullar localisation predictors:
##### \[LW 2019]
Lu, C.; Liu, Z.; Kan, B.; Gong, Y.; Ma, Z.; Wang, H. TMP-SSurface: A Deep Learning-Based Predictor for Surface Accessibility of Transmembrane Protein Residues. Crystals 2019, 9, 640.
##### \[KS 2001]
Krogh A, Larsson B, von Heijne G, Sonnhammer EL. Predicting transmembrane protein topology with a hidden Markov model: application to complete genomes. J Mol Biol. 2001;305(3):567-580. doi:10.1006/jmbi.2000.4315
##### \[NJ 2009]
Nugent, T. & Jones, D.T. (2009) Transmembrane protein topology prediction using support vector machines. BMC Bioinformatics. 10, 159. Epub
##### \[HS 1993]
K. Hofmann & W. Stoffel (1993) TMbase - A database of membrane spanning proteins segments. Biol. Chem. Hoppe-Seyler 374,166



<br /><br />
