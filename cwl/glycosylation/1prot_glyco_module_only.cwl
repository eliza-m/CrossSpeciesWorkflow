cwlVersion: v1.0
class: Workflow
  
requirements:
  SubworkflowFeatureRequirement: {}
    
inputs:

# required inputs:

   fastaFile:
     type: File


# Optional inputs:

   outputFilename: 
   # parsed data final output filename
     type: string?
     # it will be renamed in the last step
     default: "results.txt"

   outputFolder:
   # raw prediction data folder name
     type: string?
     default: "results"

   protname:
   # recommended when multiple files with the same extensions
   # exists withing the cwl running directory. 
   # Providing a baseroot name (ex: 'LEUK_RAT'), will help dealing
   # with potential confusions and files such as $protname.$predictor*
   # will be searched instead. 
   # If protname is not provided, *.$predictor* files will be searched.
   # In case of ambiguities ( none or multiple files with same extensios)
   # an error is raised.
     type: string?
     default: null

   signif: 
   # print only significant predicted sites (thresholds are predictor specific)
     type: boolean?
     default: false


outputs:

  glycosylationPredictions:
    type: Directory
    outputSource: predictAll/results

  formattedOutput:
    type: File
    outputSource: formatOutput/output


steps:

  predictAll:
    run: 1prot_glyco_predall.cwl
    in:
      fastaFile: fastaFile
    out: [results]  

  formatOutput: 
    run: ../format_output.cwl
    in:
      formattype: 
        default: "single"
      module: 
        default: "glycosylation"
      outputFilename: outputFilename
      signif: signif
      protname: protname
      inputFolder: predictAll/results

    out: [output]


