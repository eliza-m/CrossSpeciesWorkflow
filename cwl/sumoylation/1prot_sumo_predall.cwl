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

  sumogo:
    run: ../util/submit_online.cwl
    in:
      predictor: 
        default: "sumogo"
      fastaFile: fastaFile
    out: [output]

  gpssumo:
    run: ../util/submit_online.cwl
    in:
      predictor: 
        default: "gpssumo"
      fastaFile: fastaFile
    out: [output]


  retrieveFolder:
    in: 
      f1: sumogo/output
      f2: gpssumo/output
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
            "basename": inputs.f3.nameroot + "_sumo_preds",
            "listing": [inputs.f1, inputs.f2, inputs.f3]
          } };
        }
    doc: |
      Retrieve all results as a single Directory object
      that also contains the submitted Fasta sequece for
      further refference, but also needed for the output layout
