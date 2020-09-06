from __future__ import annotations
from bioservices.apps import FASTA
from dataclasses import dataclass
from species_proteins.sumoylation.Gpssumo_data import Gpssumo_data
from species_proteins.sumoylation.Sumogo_data import Sumogo_data
from species_proteins.workflow.Module_pred import Module_pred


@dataclass
class Sumoylation_pred (Module_pred):
    """
    Class that organises Sumoylation module output.
    It inherits Module_pred base class.

    Public Methods
    --------------
    Overridden methods:

    parse_all(paths: dict) -> Sumoylation_pred:
        Parses all the prediction output files.
    """

    paths: dict
    predictions: dict
    module = 'Sumoylation'
    availPredictors = ["sumogo", "gpssumo"]
    header = [
        ["sumogo", "SUMO", " "],
        ["gpssumo", "SUMO", " "],
        ["gpssumo", "SIM", " "]
    ]



    @staticmethod
    def parse_all(paths: dict) -> Sumoylation_pred:
        """
        Parses all the prediction output files.

        Parameters
        ----------
        paths :  dict
            Dictionary with raw prediction data.

        Returns
        -------
        Sumoylation_pred
            with parsed data
        """

        predictions = {}

        for prot in paths:
            for predictor in paths[prot]:

                if predictor == "sumogo":
                    data = Sumogo_data.parse(paths[prot][predictor])
                elif predictor == "gpssumo":
                    data = Gpssumo_data.parse(paths[prot][predictor])

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

        return Sumoylation_pred(paths=paths, predictions=predictions)

