cwlVersion: v1.0
class: Workflow
   
requirements:
  SubworkflowFeatureRequirement: {}
   
inputs:

# required inputs:

   uniprot:
     type: string


# Optional inputs:

   outputFilename: 
   # parsed data final output filename
     type: string?
     # it will be renamed in the last step
     default: "acet_results.txt"

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

  acetylationPredictions:
    type: Directory
    outputSource: predictAll/results

  formattedOutput:
    type: File
    outputSource: formatOutput/output


steps:

  getFasta:
    run: ../util/get_fasta.cwl
    in:
      uniprot: uniprot
      trimheader:
        default: "True"
    out: [fastaFile]  


  predictAll:
    run: 1prot_acet_predall.cwl
    in:
      fastaFile: getFasta/fastaFile
    out: [results]  

  formatOutput: 
    run: ../util/format_output.cwl
    in:
      formattype: 
        default: "single"
      module: 
        default: "acet"
      outputFilename: outputFilename
      signif: signif
      protname: protname
      inputFolder: predictAll/results

    out: [output]


