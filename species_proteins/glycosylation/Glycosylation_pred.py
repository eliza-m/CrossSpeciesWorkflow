from __future__ import annotations
from bioservices.apps import FASTA
from dataclasses import dataclass
from species_proteins.glycosylation.Netnglyc_data import Netnglyc_data
from species_proteins.glycosylation.Netoglyc_data import Netoglyc_data
from species_proteins.glycosylation.Netcglyc_data import Netcglyc_data
from species_proteins.glycosylation.Glycomine_data import Glycomine_data
from species_proteins.glycosylation.Isoglyp_data import Isoglyp_data
from species_proteins.glycosylation.Nglyde_data import Nglyde_data
from species_proteins.workflow.Module_pred import Module_pred



@dataclass
class Glycosylation_pred (Module_pred):
    """
    Class that organises Glycosylation predictions output.
    It inherits Module_pred base class.

    Public Methods
    --------------
    Overridden methods:

    parse_all(paths: dict) -> Glycosylation_pred:
        Parses all the prediction output files.
    """

    paths: dict
    predictions: dict
    availPredictors = ["netnglyc", "nglyde", "glycomineN", "netoglyc", "isoglyp", "glycomineO", "netcglyc",
                       "glycomineC"]
    header = [
        ["netnglyc", "N-glyc", " "],
        ["nglyde", "N-glyc", " "],
        ["glycomineN", "N-glyc", " "],
        ["netoglyc", "O-glyc", " "],
        ["isoglyp", "O-glyc", " "],
        ["glycomineO", "O-glyc", " "],
        ["netcglyc", "C-glyc", " "],
        ["glycomineC", "C-glyc", " "]
    ]


    @staticmethod
    def parse_all(paths: dict) -> Glycosylation_pred:
        """
        Parses all the prediction output files.

        Parameters
        ----------
        paths :  dict
            Dictionary with raw prediction data.

        Returns
        -------
        Glycosylation_pred
            with parsed data
        """

        predictions = {}

        for prot in paths:
            for predictor in paths[prot]:

                if predictor == "netnglyc":
                    data = Netnglyc_data.parse(paths[prot][predictor])
                elif predictor == "netoglyc":
                    data = Netoglyc_data.parse(paths[prot][predictor])
                elif predictor == "netcglyc":
                    data = Netcglyc_data.parse(paths[prot][predictor])
                elif predictor == "isoglyp":
                    data = Isoglyp_data.parse(paths[prot][predictor])
                elif predictor == "nglyde":
                    data = Nglyde_data.parse(paths[prot][predictor])
                elif predictor == "glycomineN":
                    data = Glycomine_data.parse(paths[prot][predictor])
                elif predictor == "glycomineO":
                    data = Glycomine_data.parse(paths[prot][predictor])
                elif predictor == "glycomineC":
                    data = Glycomine_data.parse(paths[prot][predictor])

                # adding the fasta file data
                elif predictor in ["fasta", "fsa"]:
                    # this needs to be further moved as a function that properly checks for multiprotein file 
                    # or for alignments 

                    f = FASTA()
                    f.read_fasta(paths[prot][predictor])
                    if prot in f.header :
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

        return Glycosylation_pred(paths, predictions)




