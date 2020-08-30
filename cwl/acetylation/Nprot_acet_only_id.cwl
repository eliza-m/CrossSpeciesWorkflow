
cwlVersion: v1.0
class: Workflow
  
requirements:
  ScatterFeatureRequirement: {}   
  SubworkflowFeatureRequirement: {} 
  InlineJavascriptRequirement : {}


inputs:

# Required inputs:

   idList:
     type: string[]
     doc: |
       input Uniprot ID list.
    
    
# Optional inputs:

   outputFilename: 
     type: string?
     default: "acet_results.txt"
     doc: |
       parsed data final output filename

   outputFolder:
     type: string?
     default: "acet_preds"
     doc: |
       Raw prediction data folder name

   signif: 
     type: boolean?
     default: false
     doc: |
       print only significant predicted sites (thresholds are predictor specific)


outputs:

  acetylationPredictions:
    type: Directory
    outputSource: wrap/folder
    doc: |
      A folder containing all predicted raw data

  alnFile:
    type: File
    outputSource: align/alnFile
    doc: |
      Aligned sequences

  formattedOutput:
    type: File
    outputSource: formatOutput/output
    doc: |
      Formated output file


steps:

  getFasta:
    run: ../util/get_fasta.cwl
    scatter : uniprot
    in:
      uniprot: idList
      trimheader:
        default: True
    out: [fastaFile]
    doc: |
      Gathers and prepares individual fasta files for prediction


  predictAll:
    run: 1prot_acet_predall.cwl
    scatter: fastaFile
    in:
      fastaFile: getFasta/fastaFile
    out: [results]  
    doc: |
      Run all predictors

  wrap:
    run: ../util/dirarray_to_dir.cwl
    in:
      inputFolder: predictAll/results
      outputFolder: outputFolder 
    out: [folder]
    doc: |
      Organize all prediction output as a single folder, that will become next step's input

  getMultiFasta:
    run: ../util/get_fasta_for_aln.cwl
    in:
      idList: idList
    out: [MultiFastaFile]
    doc: |
      Prepare MultiFASTA file for alignment

  align:
    run: ../util/clustalo.cwl
    in: 
      fastaFile: getMultiFasta/MultiFastaFile
    out: [alnFile]
    doc: |
      Align input sequences

  formatOutput:
    run: ../util/format_output.cwl
    in:
      formattype:
        default: "multi"
      module:
        default: "acet"
      outputFilename: outputFilename
      signif: signif
      alnFile: align/alnFile
      inputFolder: wrap/folder
    out: [output]
    doc: |
      Format final output

