cwlVersion: v1.0
class: Workflow


inputs:
   fastaFile: File




outputs:

  isoglypPred:
    type: File
    outputSource: isoglyp/output

  netnglycPred:
    type: File
    outputSource: netnglyc/output

  netcglycPred:
    type: File
    outputSource: netcglyc/output

  netoglycPred:
    type: File
    outputSource: netoglyc/output

  nglydePred:
    type: File
    outputSource: nglyde/output

  glycomineNPred:
    type: File
    outputSource: glycomineN/output

  glycomineOPred:
    type: File
    outputSource: glycomineO/output

  glycomineCPred:
    type: File
    outputSource: glycomineC/output


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
    run: ../submitonline.cwl
    in:
      predictor: 
        default: "netcglyc"
      fastaFile: fastaFile
    out: [output]

  netoglyc:
    run: ../submitonline.cwl
    in:
      predictor: 
        default: "netoglyc"
      fastaFile: fastaFile
    out: [output]

  nglyde:
    run: ../submitonline.cwl
    in:
      predictor: 
        default: "nglyde"
      fastaFile: fastaFile
    out: [output]

  glycomineN:
    run: ../submitonline.cwl
    in:
      predictor: 
        default: "glycomine"
      fastaFile: fastaFile
      predtype: 
        default: N
    out: [output]

  glycomineO:
    run: ../submitonline.cwl
    in:
      predictor: 
        default: "glycomine"
      fastaFile: fastaFile
      predtype: 
        default: O
    out: [output]

  glycomineC:
    run: ../submitonline.cwl
    in:
      predictor: 
        default: "glycomine"
      fastaFile: fastaFile
      predtype: 
        default: C
    out: [output]




