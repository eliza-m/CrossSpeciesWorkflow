from __future__ import annotations
from bioservices.apps import FASTA
from dataclasses import dataclass
from species_proteins.lipid.Gpslipid_data import Gpslipid_data
from species_proteins.workflow.Module_pred import Module_pred

@dataclass
class Lipid_pred (Module_pred):
    """Class that organises Lipid modification module output for single protein

    Attributes
    ----------

    Public Methods
    --------------
    parseall()
        Parses all the prediction output files and add the data inside the
        above attribute data structures.

    print1prot( self )
        Prints all predictions in a vertical layout
        For single protein profile layout

    printNprot( self )
        Prints all predictions in a vertical layout
        For multi protein profile layout

    """

    paths: dict
    predictions: dict
    module = 'Lipid Modification'
    availPredictors = ["gpslipid"]
    header = [
        ["gpslipid", "N-Myr", "N/A"],
        ["gpslipid", "S-Pal", "N/A"],
        ["gpslipid", "S-Ger", "N/A"],
        ["gpslipid", "S-Far", "N/A"]
    ]



    @staticmethod
    def parse_all(paths: dict) -> Lipid_pred:
        """
        Parses all the prediction output files and add the data inside the
        above attribute data structures.
        """

        predictions = {}

        for prot in paths:
            for predictor in paths[prot]:

                if predictor == "gpslipid":
                    data = Gpslipid_data.parse(paths[prot][predictor])

                # adding the fasta file data
                elif predictor in ["fasta", "fsa"]:
                    f = FASTA()
                    f.read_fasta(paths[prot][predictor])
                    if prot in f.header:
                        seq = f.sequence
                    else:
                        print("Protein name ", prot, "is not contained in the provided fasta file")
                        raise

                else:
                    print("Unknown predictor key: ", predictor)
                    raise

                if prot not in predictions:
                    predictions[prot] = {}

                if predictor not in ["fasta", "fsa"]:
                    if predictor not in predictions[prot]:
                        predictions[prot][predictor] = {}
                    predictions[prot][predictor] = data.predicted_sites[prot] if prot in data.predicted_sites else {}
            predictions[prot]['seq'] = seq

        return Lipid_pred(paths=paths, predictions=predictions)

