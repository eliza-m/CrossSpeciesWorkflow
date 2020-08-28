cwlVersion: v1.0
class: Workflow

requirements:
  SubworkflowFeatureRequirement: {}


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

  gpslipid:
    run: ../util/submit_online.cwl
    in:
      predictor: 
        default: "gpslipid"
      fastaFile: fastaFile
    out: [output]


  retrieveFolder:
    in: 
      f1: gpslipid/output
      fasta: fastaFile
  
    out: [folder]  
    run:
      
      class: ExpressionTool
      requirements:
        InlineJavascriptRequirement: {}
      inputs:
        f1: File
        fasta: File

      outputs:
        folder: Directory
      expression: |
        ${
          return {"folder": {
            "class": "Directory", 
            "basename": inputs.fasta.nameroot + "_lipid_preds",
            "listing": [inputs.f1, inputs.fasta]
          } };
        }
    doc: |
      Retrieve all results as a single Directory object
      that also contains the submitted Fasta sequece for
      further refference, but also needed for the output layout
