cwlVersion: v1.0
class: Workflow
   
requirements:
  SubworkflowFeatureRequirement: {}
  ScatterFeatureRequirement: {}
  MultipleInputFeatureRequirement: {}
   
inputs:

# Required inputs:
   fastaFile:
     type: File
     doc: |
       input single protein FASTA file.

# Optional inputs:

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

  allOutputs:
    type: File[]
    outputSource: formatAllOutputs/output
    doc: |
      Formated output file - all predictions

  acetPredictions:
    type: Directory
    outputSource: acetPredictAll/results
    doc: |
      A folder containing all acetylation predicted raw data

  glycPredictions:
    type: Directory
    outputSource: glycPredictAll/results
    doc: |
      A folder containing all glycosylation predicted raw data

  phosPredictions:
    type: Directory
    outputSource: phosPredictAll/results
    doc: |
      A folder containing all phosphorylation predicted raw data

  sumoPredictions:
    type: Directory
    outputSource: sumoPredictAll/results
    doc: |
      A folder containing all sumoylation predicted raw data

  lipidPredictions:
    type: Directory
    outputSource: lipidPredictAll/results
    doc: |
      A folder containing all lipid modification predicted raw data




steps:

  acetPredictAll:
    run: acetylation/1prot_acet_predall.cwl
    in:
      fastaFile: fastaFile
    out: [results]  
    doc: |
      Run all acet predictors

  glycPredictAll:
    run: glycosylation/1prot_glyc_predall.cwl
    in:
      fastaFile: fastaFile
    out: [results]  
    doc: |
      Run all glyc predictors

  phosPredictAll:
    run: phosphorylation/1prot_phos_predall.cwl
    in:
      fastaFile: fastaFile
    out: [results]  
    doc: |
      Run all phos predictors

  sumoPredictAll:
    run: sumoylation/1prot_sumo_predall.cwl
    in:
      fastaFile: fastaFile
    out: [results]  
    doc: |
      Run all sumo predictors

  lipidPredictAll:
    run: lipid/1prot_lipid_predall.cwl
    in:
      fastaFile: fastaFile
    out: [results]  
    doc: |
      Run all lipid predictors


  formatAllOutputs: 
    run: util/format_output.cwl
    in:
      formattype: 
        default: "single"
      module: 
        default: ["acet", "glyc", "phos", "sumo", "lipid"]
      outputFilename:
        default: "results.txt"
      signif: signif
      protname: protname
      inputFolder: 
        source: [acetPredictAll/results, glycPredictAll/results, phosPredictAll/results, sumoPredictAll/results, lipidPredictAll/results]
        linkMerge: merge_flattened
    scatter:
      - inputFolder
      - module
    scatterMethod: dotproduct
    out: [output]
    doc: |
      Formatted and merged results for each module



