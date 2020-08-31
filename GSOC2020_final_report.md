# GSOC 2020 - Final Report

## Protein sequence and structural analysis CWL pipeline for comparative biology (CSW - Cross Species Workflow)

##### Organization: Open Bioinformatics Foundation (OBF)
##### Mentors: Anton Kulaga, Dymitr Nowicki, Vlada Tyshchenko
##### Student: Eliza Martin


##### Source code: https://github.com/eliza-m/CrossSpeciesWorkflow/tree/GSOC2020


## Project scope
While there are a multitude of open source ML methods for prediction of various structural or biological related attributes, there are no open source pipelines or APIs which allow performing a one command task for running multiple/equivalent methods and join the results in a way that facilitates comparisons and further dissemination. This limits any type of structural/comparative biology analyses, as one would need to install and run >50 software and put together all the results using in-house scripts.

This project aims at developing a scalable workflow that receives the protein FASTA file and runs a series of structural and phenotype related predictors, generating a knowledge dataset that will facilitate further exploration and comparisons according to the following categories of features: secondary structure, solvent accessibility, disordered regions, PTS modifications (phosphorylation, glycosylation, lipid modification, sumoylation, etc).

Deliverables of this project consists of 8 modules for each analysis / prediction type, a Python library for processing inputs & outputs and submitting online jobs when case and CWL pipelines that will facilitate a one-line command run of all the predictors (default or custom configuration).


## Results

During the 3-month internship, the following deliverables were completed :

### 1. CWL workflows 

According to each category of predicted features: secondary structure, solvent accessibility, disordered regions, PTS modifications (phosphorylation, glycosylation, lipid modification, sumoylation, etc), prediction methods where assigned to a specific **module**. CWL workflow scripts are provided `in ${CSW_HOME}/cwl` directory, for each prediction type module, but also for an overall pipeline covering all of them.

Individual modules :
* **struct** - Structural related
* **phos**   - Phosphorylation
* **glyc**   - Glycosylation 
* **acet**   - Acetylation 
* **sumo**   - Sumoylation 
* **loc**    - Cellular localization
* **lipid**  -Lipid modification

While the following refer to **grouped** predictions modules :
* **ptm** - All Post Translation Modification modules (acet + glyc + phos + sumo + lipid)
* **all** - All modules

Specific modules can be run individually using designated CWL workflow scripts found in their corresponding module folder and can be re-used separately from the main workflow. 

Provided are CWL tools for different input types such as:

* **single protein FASTA**    : 1prot_$module_only_fasta.cwl
* **single protein ID**       : 1prot_$module_only_id.cwl
* **multi protein ID array**  : Nprot_$module_only_id.cwl

The distinction between single & multi protein mode is that in **multi** protein mode, sequences are aligned using Clustal Omega in the final output layout.  

Usage example for a specific module only for a list of protein IDs would be :
```
### INDIVIDUAL MODULES
# Structural
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/structural/Nprot_struct_only_id.cwl [YMLfile]

# Acetylation
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/acetylation/Nprot_acet_only_id.cwl [YML/JSONfile]

# Glycosylation
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/glycosylation/Nprot_glyc_only_id.cwl [YML/JSONfile]

# Phosphorylation
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/phosphorylation/Nprot_phos_only_id.cwl [YML/JSONfile]

# Lipid modification
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/lipid/Nprot_lipid_only_id.cwl [YML/JSONfile]

# Sumoylation 
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/sumoylation/Nprot_sumo_only_id.cwl [YML/JSONfile]

# Localisation
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/localisation/Nprot_loc_only_id.cwl [YML/JSONfile]

### GROUPED MODULES
# PTM predictions
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/Nprot_ptm_id.cwl [YML/JSONfile]

# ALL
cwltool --no-match-user --no-read-only --outdir [path/to/dir] ${CSW_HOME}/cwl/Nprot_all_id.cwl [YML/JSONfile]
```

### CWL workflow tests

Tests of the overall CWL workflow and individual module subworkflows can be found in `${CSW_HOME}/tests/cwl/test_modules/` directory.

:exclamation: Before running the tests please be sure the whole CSW project has been setup - see Installation & Setup section from [README.md](https://github.com/eliza-m/CrossSpeciesWorkflow/tree/GSOC2020) file :
* install prerequisites
* clone repo
* setup sequence databases symbolic links

To run all tests at once for all YML input types (single protein FASTA/ID or a list of IDs) and for all modules :
```
$ bash ${CSW_HOME}/tests/cwl/test_modules/test_all_module.sh
```
Output samples for each (sub)workflow, are found in each module's folder in `expected_output` directories.



### 2. Python API

#### Quick & dirty pipeline run 

A simplistic selection of the cwl tool can be performed directly from Python API. However it offers a very limited number of options, therefore we recommend using directly CWLtool or other workflow runner

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
                   - loc            :  Cellular localization module   [required]

  --outdir TEXT    Output directory. Default: current directory.
  --args TEXT      Arguments to be passed to cwltool.  [default: --no-match-
                   user --no-read-only]

  --parallel       Run in parallel. NOT recommended due to HTTP response
                   errors !!!  [default: False]

  --help           Show this message and exit.
```

#### Predictions merged output layout & and easy change between output layouts 

Let's assume that one has already performed an "all" module prediction pipeline for their proteins and wants to generate a formatted output only for a specific sequence and only for glycosylation related predictors.

```
$ python species_proteins/workflow/run.py format-output --format single --module glyc 
--inputfolder [path/to/predictions/dir] --protname YourID
```
As a input folder one can provide directly the overall prediction folder (that contains multiple proteins predictions) and the provided ID will be searched for (prediction output naming is $protID.predictor.*), but if the folder of the particular sequence is provided, the `--protname` argument is no longer needed. In case of ambiguities (multiple files with the same pattern were detected) an error will be raised.


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


#### Submit online jobs for a specific predictor

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

To ease FASTA files retrieval and manipulation, one can use the provided `get-fasta` CLI function. An example of retrieving sequences of a protein ID and trimming the header would be:
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
    
 
### 3. Dockerfiles

While initially we intended to provide one docker image per module, this was no longer possible due to differences between each predictor's prerequisites. Therefore, provided dockerfiles refer to individual methods.
Details about each methods docker image building and usage are found in [CONTAINERS.md](https://github.com/eliza-m/CrossSpeciesWorkflow/blob/GSOC2020/CONTAINERS.md) file.

Please note that building these images IS NOT REQUIRED for the current CWL pipeline, but could be optionally added if one wants to. As, several 3rd party predictors require registering on their website prior downloading the software, these docker containers needs to be built by each user individually. Current default pipeline uses only containers that could be uploaded to `quay.io`, but alongside the main workflow, cwl tool scripts are also provided for the methods not yet included ( `indiv_predictors` directories within each module).


## Future Work

After GSOC internship end I intend to continue adding more features to the pipeline such as:
* adding more 3rd party predictors
* adding a HTML output to ease comparisons between sequences.
* features for comparative statistical analysis such as entropy plots.


## Closing thoughts
Participating in Google Summer of Code was a great opportunity to learn a lot of new things in a such a short time, for which I am extremely thankful to the mentors, especially to Anton Kulaga for all his advices and suggestions !



