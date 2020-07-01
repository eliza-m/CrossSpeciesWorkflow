# GSOC progress journal

## Project summary
While there are a multitude of open source ML methods for prediction of various structural or biological related attributes, there are no open source pipelines or APIs which allow to performing a one command task for running multiple/equivalent methods and join the results in a way that facilitates comparisons and further dissemination. This limits any type of structural/comparative biology analyses, as one would need to install and run >50 software and put together all the results using in-house scripts.

This project aims at developing a scalable workflow that receives the protein FASTA file and runs a series of structural and phenotype related predictors, generating a knowledge dataset that will facilitate further exploration and comparisons according to the following categories of features: secondary structure, solvent accessibility, disordered regions, PTS modifications (phosphorylation, glycosylation, lipid modification, sumoylation, etc) or binding sites.

Deliverables of this project consists of 8 modules for each analysis type organized as Docker images, a Python library for processing inputs & outputs of the included methods and bash and CWL pipelines that will facilitate a one-line command run of all the predictors (default or custom configuration).

This repo intends to create an easy, user accessible and open-source tool for running a series of third party predictions software. The main focus is on:
* Dockerfiles for easy installing existing prediction software.
* a Python API for facilitating parsing and organizing each predictor's output data.
* bash and CWL pipelines that facilitates large protein sequences sets prediction jobs submissions.  


## First Month

### Tasks set for the first month :

1. Generating Dockerfiles for the predictors list chosen during the community bonding period for 2 or 3 of the modules.
2. Python API for parsing and organizing each predictor output.
3. Starting to integrate them into the bash and cwl pipelines.
3. Establishing a general framework and structure of the repo.


### Progress update :

For the first month we selected the most challenging module - Structural module - as it contains many predictors within each package that each require many dependencies as well as large protein datasets.

A. Structural module - that deals with secondary structure, relative solvent accessibility and disorder predictions:
* RaptorX-Property:
    * Dockerfile: done
    * Python classes for parsing and organizing: done
    * initial bash workflow integration: done
    * initial cwl integration: on progress (TODO: find a better way to deal with external databases that needs to be mounted in specific places inside container)
    
* Scratch1D 
    * Dockerfile: almost done (TODO: integrate DISPRO for disorder prediction because according to their documentation DISPRO requires a different version of SSPRO)
    * Python classes for parsing and organising: almost done (TODO: integrate DISPRO)
    * initial bash workflow integration: almost done (TODO: integrate DISPRO)
    * initial cwl integration: on progress.
    
* PsiPred & DisoPred
    * Dockerfile: done
    * Python classes for parsing and organising: done
    * initial bash workflow integration: done
    * initial cwl integration: on progress (TODO: deal with some hard coded paths) 
    
* Spot1D 
    * Dockerfile: on progress (TODO: the source files contain both large protein training data that should be separated and kept outside the container)
    * Python classes for parsing and organising: on progress.
    * initial bash workflow integration: on progress.
    * initial cwl integration: on progress.
    
    
B. Phosphorylation module:
* Musitedeep
    * Dockerfile: 2 dockerfiles were provided - first one is the published version but uses uses keras1 (with theano) and the second one is an updated version that uses keras2 (with tensorflow) and is a lot faster.
    * Python classes for parsing and organising: done
    * initial bash workflow integration: done
    * initial cwl integration: on progress
    
* DTU predictors: NetPhosPan & NetPhos.
These 2 predictors were added together in a single Dockerfile as they are both from DTU Health Tech and they require prior user registration and license terms agreement prior downloading the source code. Also, they are not computationally demanding
    * Dockerfile: done
    * Python classes for parsing and organising: done
    * initial bash workflow integration: done
    * initial cwl integration: on progress
    
    
### Things that need to be finished:
* refactor python parsing functions.
* refactor some of the dockerfiles to better deal with the hardcoded paths.
* generate complete and comprehensive tests for all predictors for all usecase scenarios.
* cwl workflows scripts.


### Most challenging parts:

The installation process was not straight forward for many of the predictors discussed above. Installation problems were related to :
* hardcoded paths that were solved via string replacement with `sed` within the dockerfile.
* relative paths string operations that were not updated after the final folders organization of the project.
* unspecified version of dependencies that yielded various errors.
* changed filenames without updating the code that uses them.
* incomplete conda environments provided.
* etc.



