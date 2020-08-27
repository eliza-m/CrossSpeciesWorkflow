cwlVersion: v1.0
class: Workflow
  
requirements:
  ScatterFeatureRequirement: {}   

inputs:
   idList:
     type: string[]

outputs:    
  MultiFastaFile:
    type: File
    outputSource: cat/output

steps:
  getFasta_origheadear:
    run: ../util/get_fasta.cwl
    scatter : uniprot
    in:
      uniprot: idList
      trimheader: 
        default: False
    out: [fastaFile]

  cat:
    run: ../util/cat.cwl
    in:
      files: getFasta_origheadear/fastaFile
      outputname:
        default: "prot.fasta"
    out: [output]

