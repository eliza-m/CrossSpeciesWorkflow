from __future__ import annotations
from bioservices.apps import FASTA
from dataclasses import dataclass
from pathlib import Path
import sys
from species_proteins.acetylation.Gpspail_data import Gpspail_data
from species_proteins.acetylation.Netacet_data import Netacet_data

from species_proteins.workflow.Module_pred import Module_pred

@dataclass
class Acetylation_pred (Module_pred):
    """Class that organises Acetylation module output for single protein

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
    module = 'Acetylation'
    availPredictors = ["netacet", "gpspail"]
    header = [
        ["netacet", "Nter-acet", "N/A"],
        ["gpspail", "K-acet", "CREBBP"],
        ["gpspail", "K-acet", "EP300"],
        ["gpspail", "K-acet", "HAT1"],
        ["gpspail", "K-acet", "KAT2A"],
        ["gpspail", "K-acet", "KAT2B"],
        ["gpspail", "K-acet", "KAT5"],
        ["gpspail", "K-acet", "KAT8"],
    ]


    @staticmethod
    def parse_all(paths: dict) -> Acetylation_pred:
        """
        Parses all the prediction output files and add the data inside the
        above attribute data structures.
        """

        predictions = {}

        for prot in paths:
            for predictor in paths[prot]:

                if predictor == "netacet":
                    data = Netacet_data.parse(paths[prot][predictor])
                elif predictor == "gpspail":
                    data = Gpspail_data.parse(paths[prot][predictor])

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
                    predictions[prot][predictor] = data.predicted_sites[prot]
            predictions[prot]['seq'] = seq

        return Acetylation_pred(paths=paths, predictions=predictions)

