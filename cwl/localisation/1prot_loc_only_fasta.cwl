cwlVersion: v1.0
class: Workflow


requirements:
  SubworkflowFeatureRequirement: {}

      
inputs:

# required inputs:
   fastaFile:
     type: File
     doc: |
       input single protein FASTA file.


# Optional inputs:

   outputFilename: 
     type: string?
     default: "loc_results.txt"
     doc: |
       parsed data final output filename

   protname:
     type: string?
     default: null
     doc: |
       Recommended when multiple files with the same extensions
       exists withing the cwl running directory. 
       Providing a baseroot name (ex: 'LEUK_RAT'), will help dealing
       with potential confusions and files such as $protname.$predictor*
       will be searched instead. 
       If protname is not provided, *.$predictor* files will be searched.
       In case of ambiguities ( none or multiple files with same extensios)
       an error is raised.

   signif: 
     type: boolean?
     default: false
     doc: |
       print only significant predicted sites (thresholds are predictor specific)


outputs:

  LocalisationPredictions:
    type: Directory
    outputSource: predictAll/results
    doc: |
      A folder containing all predicted raw data

  formattedOutput:
    type: File
    outputSource: formatOutput/output
    doc: |
      Formated output file

  wf_stdout:
    type: stdout

stdout: stdout.out


steps:

  predictAll:
    run: 1prot_loc_predall.cwl
    in:
      fastaFile: fastaFile
    out: [results]  
    doc: |
      Run all predictors

  formatOutput: 
    run: ../util/format_output.cwl
    in:
      formattype: 
        default: "single"
      module: 
        default: "loc"
      outputFilename: outputFilename
      signif: signif
      protname: protname
      inputFolder: predictAll/results
    out: [output]
    doc: |
      Format output


