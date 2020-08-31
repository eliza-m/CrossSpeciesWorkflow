from __future__ import annotations
from dataclasses import dataclass
from species_proteins.structural.Raptorx_data import Raptorx_data
from species_proteins.structural.Scratch1d_data import Scratch1d_data
from species_proteins.structural.Psipred_data import Psipred_data
from species_proteins.structural.Disopred_data import Disopred_data
from species_proteins.workflow.Module_pred import Module_pred


@dataclass
class Structural_pred (Module_pred):
    """
    Class that organises Structural Predictions output.
    Inherits MOdule_pred base class

    Attributes
    ----------
    Additional from base class:

    DIS_threshold : float with values between 0. and 1. (default=0.50)
            Threshold used for disorder class definition of All predictors.

    ACC_threshold: probability threshold for Scratch1D (only) rellative
            solvent prediction class definition, default=0.20


    Public Methods
    --------------
    Overridden methods:

    parse_all(paths: dict) -> Phosphorylation_pred:
        Parses all the prediction output files.

    get_layout_1prot(self: Structural_pred, protname: str, signif: bool = False) -> dict
        Overides base class method.
        Get a vertical layout of the predicted data for each protein sequences, as multiple classes that
        inherits module_pred keep only a dictionary with the predicted sites, and do not track resids and resnames.

        Arguments:
            - self          : Structural_pred [required]

            - protname      : String. Protname key to to obtain layout of. [required]

            - signif        : Boolean. If true prints only significant predicted sites. Significance thresholds are
                            predictor specific. [Optional. Default: False]

    """

    predictions: dict
    paths: dict
    DIS_threshold: float = 0.5
    ACC_threshold: float = 0.2

    module = 'Structural'
    availPredictors = ['raptorx', 'psipred', 'disopred', 'scratch1d']
    header = [
        ["raptorx", "SS", "3-class"],
      # ["scratch1d", "SS", "3-class"],
        ["psipred", "SS", "3-class"],
        ["raptorx", "SS", "8-class"],
      # ["scratch1d", "SS", "8-class"],
        ["raptorx", "ACC", "3-class"],
      # ["scratch1d", "ACC", "2-class"],
        ["raptorx", "DIS", "2-class"],
        ["disopred", "DIS", "2-class"]
    ]

    @staticmethod
    def parse_all( paths : dict, DIS_threshold: float = None, ACC_threshold: float = None ) -> Structural_pred:

        """
        Parses all the prediction output files.

        Parameters
        ----------
        paths :  dict
            Dictionary with raw prediction data.

        DIS_threshold : float with values between 0. and 1. (default=0.50)
                Threshold used for disorder class definition of All predictors.

        ACC_threshold: probability threshold for Scratch1D (only) rellative
                solvent prediction class definition, default=0.20

        Returns
        -------
        Srtuctural_pred
            with parsed data
        """

        DIS_threshold = DIS_threshold if (DIS_threshold is not None and 0.0 < DIS_threshold < 1.0) else 0.50
        ACC_threshold = ACC_threshold if (ACC_threshold is not None and 0.0 < ACC_threshold < 1.0) else 0.20

        predictions = {}
        for prot in paths:
            for predictor in paths[prot]:
                if predictor.lower() == "raptorx":
                    preddata = Raptorx_data.parse( paths[prot][predictor], DIS_threshold)
                    seq = preddata.sequence;
                elif predictor.lower() == "psipred":
                    preddata = Psipred_data.parse(paths[prot][predictor])
                elif predictor.lower() == "disopred":
                    preddata = Disopred_data.parse(paths[prot][predictor], DIS_threshold)
                elif predictor.lower() == "scratch1d":
                    preddata = Scratch1d_data.parse(paths[prot][predictor], ACC_threshold)
                else:
                    print( "Unknown predictor key: ", predictor )
                    raise

                if prot not in predictions:
                    predictions[prot] = {}
                predictions[prot][predictor] = preddata
            predictions[prot]['seq'] = seq

        return Structural_pred( predictions=predictions, paths=paths, \
                                DIS_threshold=DIS_threshold, ACC_threshold=ACC_threshold)




    def get_layout_1prot(self: Module_pred, protname: str, signif: bool = False) -> dict:
        """
        Overides base class method

        Get a vertical layout of the predicted data for each protein sequences, as multiple classes that
        inherits module_pred keep only a dictionary with the predicted sites, and do not track resids and resnames.

        Parameters
        ----------
        protname: string
            Protname key to to obtain layout of. [required]

        signif: Boolean
            If true prints only significant predicted sites. Significance thresholds are
            predictor specific. [Optional. Default: False]

        Returns
        -------
        layout: dict
            Formated layout for a specific protein sequence and predictor.
        """

        data = self.predictions[protname]
        protsize = len(data['seq'])

        layout = {}
        for entry in self.header:
            pred = entry[0]
            type = entry[1]
            details = entry[2]
            key = pred + "_" + type + "_" + details
            layout[key] = ['X' if pred not in data else '-' for resid in range(protsize)]


        layout ["raptorx_SS_3-class"] = data["raptorx"].SS3_classes
      # layout ["scratch1d_SS_3-class"] = data["scratch1d"].SS3_classes
        layout ["psipred_SS_3-class"] = data["psipred"].SS3_classes
        layout ["raptorx_SS_8-class"] = data["raptorx"].SS8_classes
      # layout ["scratch1d_SS_8-class"] = data["scratch1d"].SS8_classes
        layout ["raptorx_ACC_3-class"] = data["raptorx"].ACC3_classes
      # layout ["scratch1d_ACC_2-class"] = data["scratch1d"].ACC2_classes
        layout ["raptorx_DIS_2-class"] = data["raptorx"].DIS_classes
        layout ["disopred_DIS_2-class"] = data["disopred"].DIS_classes

        return layout

