from __future__ import annotations
from bioservices.apps import FASTA
from dataclasses import dataclass
from pathlib import Path
import sys
from species_proteins.phosphorylation.Netphospan_data import Netphospan_data
from species_proteins.phosphorylation.Netphos_data import Netphos_data
from species_proteins.phosphorylation.Musitedeep_data import Musitedeep_data
from species_proteins.workflow.Module_pred import Module_pred

@dataclass
class Phosphorylation_pred (Module_pred):
    """Class that organises Phosphorylation module output for single protein

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
    module = 'Phosphorylation'
    availPredictors = ["netphospan", "netphos", "musitedeep"]
    header = [
        ["netphospan", "STY-phos", "generic"],
        ["netphos", "STY-phos", "generic"],
        ["musitedeep", "STY-phos", "generic"]
    ]



    @staticmethod
    def parse_all(paths: dict) -> Phosphorylation_pred:
        """
        Parses all the prediction output files and add the data inside the
        above attribute data structures.
        """

        predictions = {}

        for prot in paths:
            for predictor in paths[prot]:

                if predictor == "netphospan":
                    data = Netphospan_data.parse(paths[prot][predictor])
                elif predictor == "netphos":
                    data = Netphos_data.parse(paths[prot][predictor])
                elif predictor == "musitedeepST":
                    mdST = Musitedeep_data.parse(paths[prot][predictor])
                elif predictor == "musitedeepY":
                    mdY = Musitedeep_data.parse(paths[prot][predictor])

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

                if predictor not in ["fasta", "fsa"] and 'musitedeep' not in predictor:
                    if predictor not in predictions[prot]:
                        predictions[prot][predictor] = {}
                    predictions[prot][predictor] = data.predicted_sites[prot] if prot in data.predicted_sites else {}

            predictions[prot]['seq'] = seq
            # they have different aa types, so they can be merged
            md = {**mdST.predicted_sites[prot], **mdY.predicted_sites[prot] }
            predictions[prot]['musitedeep'] = md

        return Phosphorylation_pred(paths=paths, predictions=predictions)


