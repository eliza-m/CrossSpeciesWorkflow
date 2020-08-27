
cwlVersion: v1.0
class: Workflow
  
requirements:
  ScatterFeatureRequirement: {}   
  SubworkflowFeatureRequirement: {} 
  InlineJavascriptRequirement : {}


inputs:

# required inputs:

   idList:
     type: string[]
    
    
# Optional inputs:

   outputFilename: 
   # parsed data final output filename
     type: string?
     # it will be renamed in the last step
     default: "acet_results.txt"

   outputFolder:
   # raw prediction data folder name
     type: string?
     default: "acet_results"

   signif: 
   # print only significant predicted sites (thresholds are predictor specific)
     type: boolean?
     default: false


outputs:

  acetylationPredictions:
    type: Directory
    outputSource: organize/folder

  alnFile:
    type: File
    outputSource: align/alnFile

  formattedOutput:
    type: File
    outputSource: formatOutput/output


steps:

  # Get trimmed individual fasta files for prediction input
  getFasta:
    run: ../util/get_fasta.cwl
    scatter : uniprot
    in:
      uniprot: idList
      trimheader:
        default: "True"
    out: [fastaFile]

  # Run all predictions
  predictAll:
    run: 1prot_acet_predall.cwl
    scatter: fastaFile
    in:
      fastaFile: getFasta/fastaFile
    out: [results]  

  # Organize all prediction output as a single folder
  organize:
    in:
      results: predictAll/results
      outputFolder: outputFolder
    out: [folder]
    run:
      class: ExpressionTool
      id: "organize"
      inputs:
        results: Directory[]
        outputFolder :
          type: string?
          default: "acet_results"
      outputs:
        folder: Directory
      expression: |
        ${
          var folder = {
            "class": "Directory",
            "basename": inputs.outputFolder,
            "listing": inputs.results
          };
          return { "folder": folder };
        }

  # Get single file fasta for alignments
  getMultiFasta:
    run: ../util/get_fasta_for_aln.cwl
    in:
      idList: idList
    out: [MultiFastaFile]

  # Align sequences
  align:
    run: ../util/clustalo.cwl
    in: 
      fastaFile: getMultiFasta/MultiFastaFile
    out: [alnFile]

  # Format overall output
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
      inputFolder: organize/folder
    out: [output]

