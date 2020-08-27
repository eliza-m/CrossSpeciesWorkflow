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

  isoglyp:
    run: indiv_predictors/isoglyp_docker.cwl
    in:
      fastaFile: fastaFile
    out: [output] 

  netnglyc:
    run: ../util/submit_online.cwl
    in:
      predictor: 
        default: "netnglyc"
      fastaFile: fastaFile
    out: [output]

  netcglyc:
    run: ../util/submit_online.cwl
    in:
      predictor: 
        default: "netcglyc"
      fastaFile: fastaFile
    out: [output]

  netoglyc:
    run: ../util/submit_online.cwl
    in:
      predictor: 
        default: "netoglyc"
      fastaFile: fastaFile
    out: [output]

  nglyde:
    run: ../util/submit_online.cwl
    in:
      predictor: 
        default: "nglyde"
      fastaFile: fastaFile
    out: [output]

  glycomineN:
    run: ../util/submit_online.cwl
    in:
      predictor: 
        default: "glycomine"
      fastaFile: fastaFile
      predtype: 
        default: N
    out: [output]

  glycomineO:
    run: ../util/submit_online.cwl
    in:
      predictor: 
        default: "glycomine"
      fastaFile: fastaFile
      predtype: 
        default: O
    out: [output]

  glycomineC:
    run: ../util/submit_online.cwl
    in:
      predictor: 
        default: "glycomine"
      fastaFile: fastaFile
      predtype: 
        default: C
    out: [output]


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
            "basename": inputs.f9.nameroot + "_glyc_preds",
            "listing": [inputs.f1, inputs.f2, inputs.f3, inputs.f4, inputs.f5, inputs.f6, inputs.f7, inputs.f8, inputs.f9]
          } };
        }

    doc: |
      Retrieve all results as a single Directory object
      that also contains the submitted Fasta sequece for
      further refference, but also needed for the output layout
      Also this is an easy way to be sure that formatting steps 
      will be executed lastly
