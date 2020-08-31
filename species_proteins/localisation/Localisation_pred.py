from __future__ import annotations
from bioservices.apps import FASTA
from dataclasses import dataclass
from species_proteins.localisation.Tmpred_data import Tmpred_data
from species_proteins.localisation.Tmhmm_data import Tmhmm_data
from species_proteins.workflow.Module_pred import Module_pred


@dataclass
class Localisation_pred (Module_pred):
    """
    Class that organises Localisation module output.
    It inherits Module_pred base class.

    Public Methods
    --------------
    Overridden methods:

    parse_all(paths: dict) -> Localisation_pred:
        Parses all the prediction output files.
    """

    paths: dict
    predictions: dict
    module = 'Localisation'
    availPredictors = ["tmpred", "tmhmm"]
    header = [
        ["tmpred", "TM", "3-class"],
        ["tmhmm", "TM", "3-class"]
    ]

    @staticmethod
    def parse_all(paths: dict) -> Localisation_pred:
        """
        Parses all the prediction output files.

        Parameters
        ----------
        paths :  dict
            Dictionary with raw prediction data.

        Returns
        -------
        Localisation_pred
            with parsed data
        """

        predictions = {}

        for prot in paths:
            for predictor in paths[prot]:
                if predictor == "tmhmm":
                    data = Tmhmm_data.parse(paths[prot][predictor])
                elif predictor == "tmpred":
                    data = Tmpred_data.parse(paths[prot][predictor])

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

        return Localisation_pred(paths=paths, predictions=predictions)

