cwlVersion: v1.0
class: Workflow
   
requirements:
  SubworkflowFeatureRequirement: {}
  ScatterFeatureRequirement: {}
  MultipleInputFeatureRequirement: {}
  InlineJavascriptRequirement : {}

   
inputs:

# Required inputs:

   idList:
     type: string[]
     doc: |
       input Uniprot ID list.

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

  alnFile:
    type: File
    outputSource: align/alnFile
    doc: |
      Formated output file - all predictions

  structPredictions:
    type: Directory
    outputSource: structwrap/folder
    doc: |
      A folder containing all structural predicted raw data

  acetPredictions:
    type: Directory
    outputSource: acetwrap/folder
    doc: |
      A folder containing all acetylation predicted raw data

  glycPredictions:
    type: Directory
    outputSource: glycwrap/folder
    doc: |
      A folder containing all glycosylation predicted raw data

  phosPredictions:
    type: Directory
    outputSource: phoswrap/folder
    doc: |
      A folder containing all phosphorylation predicted raw data

  sumoPredictions:
    type: Directory
    outputSource: sumowrap/folder
    doc: |
      A folder containing all sumoylation predicted raw data

  lipidPredictions:
    type: Directory
    outputSource: lipidwrap/folder
    doc: |
      A folder containing all lipid modification predicted raw data

  locPredictions:
    type: Directory
    outputSource: locwrap/folder
    doc: |
      A folder containing all localisation predicted raw data


steps:

  getFasta:
    run: util/get_fasta.cwl
    scatter : uniprot
    in:
      uniprot: idList
      trimheader:
        default: True
    out: [fastaFile]
    doc: |
      Gathers and prepares individual fasta files for prediction


  structPredictAll:
    run: structural/1prot_struct_predall.cwl
    scatter: fastaFile
    in:
      fastaFile: getFasta/fastaFile
      U50folder: U50folder
      U20folder: U20folder
    out: [results]  
    doc: |
      Run all struct predictors

  acetPredictAll:
    run: acetylation/1prot_acet_predall.cwl
    scatter: fastaFile
    in:
      fastaFile: getFasta/fastaFile
    out: [results]  
    doc: |
      Run all acet predictors

  glycPredictAll:
    run: glycosylation/1prot_glyc_predall.cwl
    scatter: fastaFile
    in:
      fastaFile: getFasta/fastaFile
    out: [results]  
    doc: |
      Run all glyc predictors

  phosPredictAll:
    run: phosphorylation/1prot_phos_predall.cwl
    scatter: fastaFile
    in:
      fastaFile: getFasta/fastaFile
    out: [results]  
    doc: |
      Run all phos predictors

  sumoPredictAll:
    run: sumoylation/1prot_sumo_predall.cwl
    scatter: fastaFile
    in:
      fastaFile: getFasta/fastaFile
    out: [results]  
    doc: |
      Run all sumo predictors

  lipidPredictAll:
    run: lipid/1prot_lipid_predall.cwl
    scatter: fastaFile
    in:
      fastaFile: getFasta/fastaFile
    out: [results]  
    doc: |
      Run all lipid predictors

  locPredictAll:
    run: localisation/1prot_loc_predall.cwl
    scatter: fastaFile
    in:
      fastaFile: getFasta/fastaFile
    out: [results]  
    doc: |
      Run all loc predictors


  structwrap:
    run: util/dirarray_to_dir.cwl
    in:
      inputFolder: structPredictAll/results
      outputFolder: 
        default: "struct_preds"
    out: [folder]

  acetwrap:
    run: util/dirarray_to_dir.cwl
    in:
      inputFolder: acetPredictAll/results
      outputFolder: 
        default: "acet_preds"
    out: [folder]

  glycwrap:
    run: util/dirarray_to_dir.cwl
    in:
      inputFolder: glycPredictAll/results
      outputFolder: 
        default: "glyc_preds"
    out: [folder]

  phoswrap:
    run: util/dirarray_to_dir.cwl
    in:
      inputFolder: phosPredictAll/results
      outputFolder: 
        default: "phos_preds"
    out: [folder]

  sumowrap:
    run: util/dirarray_to_dir.cwl
    in:
      inputFolder: sumoPredictAll/results
      outputFolder: 
        default: "sumo_preds"
    out: [folder]

  lipidwrap:
    run: util/dirarray_to_dir.cwl
    in:
      inputFolder: lipidPredictAll/results
      outputFolder: 
        default: "lipid_preds"
    out: [folder]

  locwrap:
    run: util/dirarray_to_dir.cwl
    in:
      inputFolder: locPredictAll/results
      outputFolder: 
        default: "loc_preds"
    out: [folder]


  getMultiFasta:
    run: util/get_fasta_for_aln.cwl
    in:
      idList: idList
    out: [MultiFastaFile]
    doc: |
      Prepare MultiFASTA file for alignment

  align:
    run: util/clustalo.cwl
    in: 
      fastaFile: getMultiFasta/MultiFastaFile
    out: [alnFile]
    doc: |
      Align input sequences


  formatAllOutputs: 
    run: util/format_output.cwl
    in:
      formattype: 
        default: "multi"
      module: 
        default: ["struct", "acet", "glyc", "phos", "sumo", "lipid", "loc"]
      outputFilename:
        default: "results.txt"
      signif: signif
      inputFolder: 
        source: [structwrap/folder, acetwrap/folder, glycwrap/folder, phoswrap/folder, sumowrap/folder, lipidwrap/folder, locwrap/folder]
        linkMerge: merge_flattened
      alnFile: align/alnFile
    scatter:
      - inputFolder
      - module
    scatterMethod: dotproduct
    out: [output]
    doc: |
      Final output results formatted for each module



