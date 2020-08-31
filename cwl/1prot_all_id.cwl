cwlVersion: v1.0
class: Workflow
   
requirements:
  SubworkflowFeatureRequirement: {}
  ScatterFeatureRequirement: {}
  MultipleInputFeatureRequirement: {}
   
inputs:

# Required inputs:
   uniprot:
     type: string
     doc: |
       input Uniprot ID.

# Optional inputs:

   U20folder:
     type: Directory?
     default:
       class: Directory
       location: ../databases/uniprot20_2016_02
     doc: |
       Uniprot20 database folder.

   U50folder:
     type: Directory? 
     default:
       class: Directory
       location: ../databases/uniref50
     doc: |
       UniRef50 blast database folder.

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

  structPredictions:
    type: Directory
    outputSource: structPredictAll/results
    doc: |
      A folder containing all structural predicted raw data

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

  locPredictions:
    type: Directory
    outputSource: locPredictAll/results
    doc: |
      A folder containing all localisation predicted raw data





steps:

  getFasta:
    run: util/get_fasta.cwl
    in:
      uniprot: uniprot
      trimheader:
        default: True
    out: [fastaFile]  
    doc: |
      Gathers and prepares individual fasta files for prediction


  structPredictAll:
    run: structural/1prot_struct_predall.cwl
    in:
      fastaFile: getFasta/fastaFile
      U50folder: U50folder
      U20folder: U20folder
    out: [results]  
    doc: |
      Run all struct predictors

  acetPredictAll:
    run: acetylation/1prot_acet_predall.cwl
    in:
      fastaFile: getFasta/fastaFile
    out: [results]  
    doc: |
      Run all acet predictors

  glycPredictAll:
    run: glycosylation/1prot_glyc_predall.cwl
    in:
      fastaFile: getFasta/fastaFile
    out: [results]  
    doc: |
      Run all glyc predictors

  phosPredictAll:
    run: phosphorylation/1prot_phos_predall.cwl
    in:
      fastaFile: getFasta/fastaFile
    out: [results]  
    doc: |
      Run all phos predictors

  sumoPredictAll:
    run: sumoylation/1prot_sumo_predall.cwl
    in:
      fastaFile: getFasta/fastaFile
    out: [results]  
    doc: |
      Run all sumo predictors

  lipidPredictAll:
    run: lipid/1prot_lipid_predall.cwl
    in:
      fastaFile: getFasta/fastaFile
    out: [results]  
    doc: |
      Run all lipid predictors

  locPredictAll:
    run: localisation/1prot_loc_predall.cwl
    in:
      fastaFile: getFasta/fastaFile
    out: [results]  
    doc: |
      Run all loc predictors

  formatAllOutputs: 
    run: util/format_output.cwl
    in:
      formattype: 
        default: "single"
      module: 
        default: ["struct", "acet", "glyc", "phos", "sumo", "lipid", "loc"]
      outputFilename:
        default: "results.tsv"
      signif: signif
      protname: protname
      inputFolder: 
        source: [structPredictAll/results, acetPredictAll/results, glycPredictAll/results, phosPredictAll/results, sumoPredictAll/results, lipidPredictAll/results, locPredictAll/results]
        linkMerge: merge_flattened
    scatter:
      - inputFolder
      - module
    scatterMethod: dotproduct
    out: [output]
    doc: |
      Formatted and merged results for each module




