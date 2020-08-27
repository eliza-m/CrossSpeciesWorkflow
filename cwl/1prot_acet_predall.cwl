cwlVersion: v1.0
class: Workflow

requirements:
  SubworkflowFeatureRequirement: {}


inputs:

# Required inputs:

   fastaFile:
     type: File

outputs:

  results:
    type: Directory
    outputSource: retrieveFolder/folder


steps:

  netacet:
    run: ../util/submit_online.cwl
    in:
      predictor: 
        default: "netacet"
      fastaFile: fastaFile
    out: [output]

  gpspail:
    run: ../util/submit_online.cwl
    in:
      predictor: 
        default: "gpspail"
      fastaFile: fastaFile
    out: [output]


  # retrieve all results as a single Directory object
  retrieveFolder:
    in: 
      f1: netacet/output
      f2: gpspail/output
      f3: fastaFile
  
    out: [folder]  
    run:
      
      class: ExpressionTool
      requirements:
        InlineJavascriptRequirement: {}
      inputs:
        f1: File
        f2: File
        f3: File

      outputs:
        folder: Directory
      expression: |
        ${
          return {"folder": {
            "class": "Directory", 
            "basename": inputs.f3.nameroot + "_acet_preds",
            "listing": [inputs.f1, inputs.f2, inputs.f3]
          } };
        }

