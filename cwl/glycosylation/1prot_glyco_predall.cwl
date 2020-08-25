cwlVersion: v1.0
class: Workflow

requirements:
  SubworkflowFeatureRequirement: {}


inputs:

# Required inputs:

   fastaFile:
     type: File

   outputFolder:
   # prediction data folder contaiing all raw files
     type: string?
     default: "results"


outputs:

  results:
    type: Directory
    outputSource: retrieveFolder/folder


steps:

  isoglyp:
    run: indiv_predictors/isoglyp_docker.cwl
    in:
      fastaFile: fastaFile
    out: [output] 

  netnglyc:
    run: ../submitonline.cwl
    in:
      predictor: 
        default: "netnglyc"
      fastaFile: fastaFile
    out: [output]

  netcglyc:
    run: ../submit_online.cwl
    in:
      predictor: 
        default: "netcglyc"
      fastaFile: fastaFile
    out: [output]

  netoglyc:
    run: ../submit_online.cwl
    in:
      predictor: 
        default: "netoglyc"
      fastaFile: fastaFile
    out: [output]

  nglyde:
    run: ../submit_online.cwl
    in:
      predictor: 
        default: "nglyde"
      fastaFile: fastaFile
    out: [output]

  glycomineN:
    run: ../submit_online.cwl
    in:
      predictor: 
        default: "glycomine"
      fastaFile: fastaFile
      predtype: 
        default: N
    out: [output]

  glycomineO:
    run: ../submit_online.cwl
    in:
      predictor: 
        default: "glycomine"
      fastaFile: fastaFile
      predtype: 
        default: O
    out: [output]

  glycomineC:
    run: ../submit_online.cwl
    in:
      predictor: 
        default: "glycomine"
      fastaFile: fastaFile
      predtype: 
        default: C
    out: [output]


  # retrieve all results as a single Directory object
  retrieveFolder:
    in: 
      f1: isoglyp/output
      f2: netnglyc/output
      f3: netoglyc/output
      f4: netcglyc/output
      f5: glycomineN/output
      f6: glycomineO/output
      f7: glycomineC/output
      f8: nglyde/output
      f9: fastaFile

      outputFolder: outputFolder
    
  
    out: [folder]  
    run:
      
      class: ExpressionTool
      requirements:
        InlineJavascriptRequirement: {}
      inputs:
        outputFolder: string
        f1: File
        f2: File
        f3: File
        f4: File
        f5: File
        f6: File
        f7: File
        f8: File
        f9: File

      outputs:
        folder: Directory
      expression: |
        ${
          return {"folder": {
            "class": "Directory", 
            "basename": inputs.outputFolder,
            "listing": [inputs.f1, inputs.f2, inputs.f3, inputs.f4, inputs.f5, inputs.f6, inputs.f7, inputs.f8, inputs.f9]
          } };
        }

