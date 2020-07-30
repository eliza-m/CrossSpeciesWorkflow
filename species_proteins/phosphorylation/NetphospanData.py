from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import os, sys

@dataclass
class NetphospanData:
    """Class that parses Netphospan prediction output data.

    Parameters
    ----------

    Attributes
    ----------
    predictedSites : Dictionary
        predictedSites [ protein name ][ start resid ] : array of entry dict
        entry dict has the following keys:

        # Common to all PTS predictors
            seq : string (stretch of the predicted sequence)
            start : starting residue id
            end : ending residue id
            isSignif : bool (is the method's specific scoring indicating a
                            potentially significant result)
            score : float (probability)
            type : string (generic or a specific kinase)
            predictor : string (for cases where multiple predictors are available)

    Public Methods
    --------------
    parse( outputFile : path ) -> Netphospan
        Parses the Netphos prediction output file and add the data inside the
        above attribute data structure.

    """

    predictedSites : dict = field(default_factory=dict)

    @staticmethod
    def parse(outputFile: Path) -> NetphospanData :

        data = NetphospanData()

        try:
            f = open(outputFile, 'r')

            lines = f.readlines()
            for line in lines:
                l = line.split()
                if len(l) == 5 and l[0]!='pos' and l[0][0]!='#' :

                    protname = l[3]
                    if protname not in data.predictedSites:
                        data.predictedSites[protname] = {}

                    peptide = l[2]
                    peplen = len(peptide)
                    aa = peptide[ int(peplen/2) ]

                    resid = int(l[0])
                    score = round(float(l[4]), 3)

                    isSignif = (score >= 0.5)
                    type = l[1]

                    if resid not in data.predictedSites[protname]:
                        data.predictedSites[protname][resid] = []

                    data.predictedSites[protname][resid].append({
                        "seq": aa,
                        "start": resid,
                        "end": resid,
                        "isSignif": isSignif,
                        "score": score,
                        "type": type,
                        "predictor": "netphospan"
                    })


        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return data


