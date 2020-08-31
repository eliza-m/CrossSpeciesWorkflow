cwlVersion: v1.0
class: Workflow
  
requirements:
  ScatterFeatureRequirement: {}   

inputs:
   idList:
     type: string[]
     doc: |
       input Uniprot IDs.

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

doc: |
  Tool runs species_proteins/run.py get-fasta to retrieve a single multi FASTA file
  required for the alignment tool. Also it will contain original headers.
