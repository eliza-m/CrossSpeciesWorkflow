cwlVersion: v1.0
class: Workflow

requirements:
  SubworkflowFeatureRequirement: {}
  StepInputExpressionRequirement: {}


inputs:
  fastaFile:
    type: File
    doc: |
      input single protein FASTA file.


outputs:

  results:
    type: Directory
    outputSource: retrieveFolder/folder
    doc: |
      A folder containing all predicted raw data

steps:

  netphos:
    run: ../util/submit_online.cwl
    in:
      predictor: 
        default: "netphos"
      fastaFile: fastaFile
    out: [output]

  netphospan:
    run: ../util/submit_online.cwl
    in:
      predictor: 
        default: "netphospan"
      fastaFile: fastaFile
    out: [output]

  musitedeepST:
    run: indiv_predictors/musitedeep_docker.cwl
    in:
      fastaFile: fastaFile
      outputNameroot: 
        valueFrom: $(inputs.fastaFile.nameroot)
      generalMode: 
        default: general
      residues:
        default: S,T
    out: [output] 

  musitedeepY:
    run: indiv_predictors/musitedeep_docker.cwl
    in:
      fastaFile: fastaFile
      outputNameroot: 
        valueFrom: $(inputs.fastaFile.nameroot)
      generalMode: 
        default: general
      residues:
        default: Y
    out: [output] 


  retrieveFolder:
    in: 
      f1: netphos/output
      f2: netphospan/output
      f3: musitedeepST/output
      f4: musitedeepY/output
      fasta: fastaFile
  
    out: [folder]  
    run:
      
      class: ExpressionTool
      requirements:
        InlineJavascriptRequirement: {}
      inputs:
        f1: File
        f2: File
        f3: File
        f4: File
        fasta: File

      outputs:
        folder: Directory
      expression: |
        ${
          return {"folder": {
            "class": "Directory", 
            "basename": inputs.fasta.nameroot + "_phos_preds",
            "listing": [inputs.f1, inputs.f2, inputs.f3, inputs.f4, inputs.fasta]
          } };
        }
    doc: |
      Retrieve all results as a single Directory object
      that also contains the submitted Fasta sequece for
      further refference, but also needed for the output layout
