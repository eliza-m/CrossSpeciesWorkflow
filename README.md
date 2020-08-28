# Cross Species Structural, Post translational modifications and Functional protein predictions workflow

Content summary:
* [General Info](#general-info)
* [Project status](#project-status)
* [Installation & usage](#installation-\&-usage)
* [Running-CWL-workflows](#running-cwl-workflows)
* [Python API](#python-api)
* [Prediction Modules](#prediction-modules)
* [References](#references)


# General Info
While there are a multitude of open source ML methods for prediction of various structural or biological related attributes, there are no open source pipelines or APIs which allow performing a one command task for running multiple/equivalent methods and join the results in a way that facilitates comparisons and further dissemination. This limits any type of structural/comparative biology analyses, as one would need to install and run >50 software and put together all the results using in-house scripts.

This project aims at developing a scalable workflow that receives the protein FASTA file and runs a series of structural and phenotype related predictors, generating a knowledge dataset that will facilitate further exploration and comparisons according to the following categories of features: secondary structure, solvent accessibility, disordered regions, PTS modifications (phosphorylation, glycosylation, lipid modification, sumoylation, etc).

Deliverables of this project consists of 8 modules for each analysis / prediction type, a Python library for processing inputs & outputs and submitting online jobs when case and CWL pipelines that will facilitate a one-line command run of all the predictors (default or custom configuration).

This repo intends to create an easy, user accesible and open-source tool for running a series of third party predictions software. The main focus is on:
* Dockerfiles for easy installing existing prediction software.
* Python API for facilitating parsing and organising each predictor's output data.
* CWL pipelines that facilitates large protein sequences sets prediction jobs submissions and parallelisation.  



# Project status 
The project is currently under development :exclamation:. Some features might not yet won't work properly ::exclamation::

The project was tested so far only on native Ubuntu 18 .

Currently there are 3 main modules that deal with:
* A. Structural related
* B. Phosphorylation
* C. Glycosylaytion 
* D. Acetylation 
* E. Sumoylation 
* F. Cellular localisation
* G. Lipid modification

=======
Many features in this development branch are not yet implemented and won't work properly ::exclamation::


# Installation & Setup 

## Requirements before using CrossSpeciesWorkflow: #
To run CWL workflows you can use any CWL runner of your choice. By default (and also for the ease of debugging) we used CWLtool.
Some of the docker images used in the pipeline have complex license, hence you have to build them yourself (the instructions are given)

#### Install Prerequisites
* Docker client: 
    * Docker Desktop for Windows or MAC - [click](https://www.docker.com/products/docker-desktop)
    * docker-ce-cli for Linux - [click](docs.docker.com/install/linux/docker-ce/ubuntu/)
* cwltool - [click](https://github.com/common-workflow-language/cwltool)
* Python3.8 and above


## Clone repo
```
git clone https://github.com/eliza-m/CrossSpeciesWorkflow.git
```
Please set the CrossSpeciesWorkflow project home variable and add it to `.bashrc` :
```
export CSW_HOME=/path/to/CrossSpeciesWorkflow/project/home
cd CSW_HOME
```
Conda environment that has cwltool and python is also provided.
```bash
conda env create -f environment.yaml
```
The python code in this project is published as a conda package.
```bash
conda activate species_proteins
python setup.py install
```

## Setup sequence databases

Structural module predictors require downloading and setting up different protein databases. Links for download are provided bellow
* RaptorX
    * Uniprot20 : http://wwwuser.gwdg.de/~compbiol/data/hhsuite/databases/hhsuite_dbs/old-releases/uniprot20_2016_02.tgz
* Psipred & Disopred:
    * UniRef50/UniRef90 FASTA format : uniprot.org/downloads. 

Afterwards, for UniRef50/UniRef90 a blast database needs to be created (this steps need to be done only once, afterwards the database can be used or moved anywhere):
```bash
# if you do not habe BLAST+ installed run:
sudo apt-get install ncbi-blast+
	
# go to the place where Uniref fasta file is being stored (change the path bellow accordingly):
cd /Place/where/UnirefX.fasta/file/is/stored
	
# create database (this might take a while from several minutes to one hour)
makeblastdb -dbtype prot -in uniref50.fasta
```



# Running CWL workflows #

### Main workflow

......TO BE UPDATED...


### Specifil modules

Specific modules can be run individually using designated CWL workflow scripts found in their corresponding modules folder.
Provided are tools for different input types such as:

* single protein FASTA    : 1prot_$module_only_fasta.cwl
* single protein ID       : 1prot_$module_only_id.cwl
* multi protein ID array  : Nprot_$module_only_id.cwl

The disctinction between single & multi protein mode is that in multi protein mode, sequences are aligned using Clustal Omega in the final output layout.  

Example YML input files are provided within ${CSW_HOME}/tests/cwl , alongside with output samples for each cwl workflow.

Usage example for a specific module only:
```
# Acetylation
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/acetylation/Nprot_acet_only_id.cwl 
/tests/cwl/Nprot_id.yml

# Glycosylation
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/glycosylation/Nprot_glyc_only_id.cwl 
/tests/cwl/Nprot_id.yml

# Phosphorylation
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/phosphorylation/Nprot_phos_only_id.cwl 
/tests/cwl/Nprot_id.yml

# Lipid modification
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/lipid/Nprot_lipid_only_id.cwl 
/tests/cwl/Nprot_id.yml

# Sumoylation 
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/sumoylation/Nprot_sumo_only_id.cwl 
/tests/cwl/Nprot_id.yml

...
```

# Python API

## Command-line options

### Quick & dirty pipeline run 

A simplist selection of the cwl tool can be performed directly from Python API. However it offers a very limited number of options, therefore we recommend using directly CWLtool or other workflow runner

```bash
# Full pipeline & one protein example
$ python species_proteins/workflow/run.py pipeline --cwlinput tests/cwl/1prot_id.yml --mode single 
--module all --outdir [path/to/dir]  

# Acetylation module & multi protein example
$ python species_proteins/workflow/run.py pipeline --cwlinput tests/cwl/Nprot_id.yml --mode multi 
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
                   - all_nonstruct  :  All except structural module (which is slow)
                   - ptsmod         :  All Post Translation modifications ( glyc + acet + phos + sumo + lipid)
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

  --parallel       Run in parallel  [default: False]
  --help           Show this message and exit.
```

### Predictions merged output layout & and easy change between output layouts 

Let's assume that you have already performed an "all" module prediction pipeline for your proteins and you want to generate a formatted output only for a specific sequence and only for glycosylation related predictors.

```
$ python species_proteins/workflow/run.py format-output --format single --module glyc 
--inputfolder [path/to/predictions/dir] --protname YourID
```
As a input folder you can provide directly the overall prediction folder (that containes multiple proteins predictions) and the provided ID will be searched for (prediction output naming is $protID.predictor.*), but if you provide directly the folder of the desired protein the `--protname` argument is no longer needed.


For other options, see help menu:
```
$ python species_proteins/workflow/run.py format-output --help
Usage: run.py format-output [OPTIONS]

  Generates a vertical formatted layout of all predicted outputs. If 'multi'
  protein format is selected, sequences are shown aligned.

Options:
  --format TEXT       "single" or "multi" protein layout  [required]
  --module TEXT       Prediction module - accepted values:
                      - all            :  All modules
                      - all_nonstruct  :  All except structural module (which is slow)
                      - ptsmod         :  All Post Translation modifications ( glyc + acet + phos + sumo + lipid)
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
                      for PTS predictors (significance thresholds are method
                      specific.)  [default: False]

  --protname TEXT     Only for single protein format, when within the specified input
                      folder there are multiple files with the same extension, a basename of the protein should be provided.
                      Example: protname.predictor.out; Default: null

  --alnfile TEXT      Required for "multi" protein layout.
  --help              Show this message and exit.
```


### Submit online jobs for a specific predictor

Usage example:
```
$ python species_proteins/workflow/run.py submit-online --input MyPROT.fasta --predictor gpslipid --output MyPROT.gpslipid.html 
```
Some online predictors accept multiFASTA input, some do not...

Other options:
```
$ python species_proteins/workflow/run.py submit-online --help
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
                    - Cellular localisation: 'tmhmm'  [required]

  --help            Show this message and exit.
```


## Prediction Modules 













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
