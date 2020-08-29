cwlVersion: v1.0
class: Workflow

requirements:
  SubworkflowFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  InlineJavascriptRequirement: {}


inputs:
 fastaFile:
    type: File
    doc: |
      input single protein FASTA file.

 U20folder:
    type: Directory?
    default:
      class: Directory
      location: ../../databases/uniprot20_2016_02

 U50folder:
    type: Directory? 
    default:
      class: Directory
      location: ../../databases/uniref50
    doc: |
      UniRef50 blast database folder.


outputs:

  results:
    type: Directory
    outputSource: retrieveFolder/folder
    doc: |
      A folder containing all predicted raw data


steps:

  raptorx:
    run: indiv_predictors/raptorx_docker.cwl
    in:
      DBfolder: U20folder
      DBname: 
        default: "uniprot20_2016_02"
      fastaFile: fastaFile
    out: [output]

  psipred:
    run: indiv_predictors/psipred_docker.cwl
    in:
      DBfolder: U50folder
      DBname: 
        default: "uniref50.fasta"
      fastaFile: fastaFile
    out: [output]

  disopred:
    run: indiv_predictors/disopred_docker.cwl
    in:
      DBfolder: U50folder
      DBname: 
        default: "uniref50.fasta"
      fastaFile: fastaFile
    out: [output]

  scratch1d:
    run: indiv_predictors/scratch1d_docker.cwl
    in:
      outputNameroot:
        valueFrom: $(inputs.fastaFile.nameroot)
      fastaFile: fastaFile
    out: [output]


  raptorx_folder:
    run: ../util/filearray_to_dir.cwl
    in:
      files: raptorx/output
      foldername: 
        valueFrom: $(inputs.files[0].nameroot).raptorx.pred
    out: [folder]

  psipred_folder:
    run: ../util/filearray_to_dir.cwl
    in:
      files: psipred/output
      foldername:
        valueFrom: $(inputs.files[0].nameroot).psipred.pred
    out: [folder]

  disopred_folder:
    run: ../util/filearray_to_dir.cwl
    in:
      files: disopred/output
      foldername:
        valueFrom: $(inputs.files[0].nameroot).disopred.pred
    out: [folder]

  scratch1d_folder:
    run: ../util/filearray_to_dir.cwl
    in:
      files: scratch1d/output
      foldername:
        valueFrom: $(inputs.files[0].nameroot).scratch1d.pred
    out: [folder]


  retrieveFolder:
    in: 
      f1: raptorx_folder/folder
      f2: psipred_folder/folder
      f3: disopred_folder/folder
      f4: scratch1d_folder/folder
      fasta: fastaFile
  
    out: [folder]  
    run:
      
      class: ExpressionTool
      requirements:
        InlineJavascriptRequirement: {}
      inputs:
        f1: Directory
        f2: Directory
        f3: Directory
        f4: Directory
        fasta: File

      outputs:
        folder: Directory
      expression: |
        ${
          return {"folder": {
            "class": "Directory", 
            "basename": inputs.fasta.nameroot + "_structural_preds",
            "listing": [inputs.f1, inputs.f2, inputs.f3, inputs.f4, inputs.fasta]
          } };
        }
    doc: |
      Retrieve all results as a single Directory object
      that also contains the submitted Fasta sequece for
      further refference, but also needed for the output layout
