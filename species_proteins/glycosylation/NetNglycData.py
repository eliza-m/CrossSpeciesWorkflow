from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import os, sys

@dataclass
class NetNglycData:
    """Class that parses NetNglyc prediction output data.

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
            score : float (interpretation differs between methods)
            type : string (N-glyc)
            predictor : string (for cases where multiple predictors are available)

    Public Methods
    --------------
    parse( outputFile : path ) -> NetNglyc
        Parses the NetNglyc prediction output file and add the data inside the
        above attribute data structure.

    """

    predictedSites : dict = field(default_factory=dict)

    @staticmethod
    def parse(outputFile: Path) -> NetNglycData :

        data = NetNglycData()

        try:
            f = open(outputFile, 'r')

            lines = f.readlines()
            for line in lines:
                l = line.split()
                if len(l) == 6 and l[0][0:6] != "Signal" :
                    protname = l[0]
                    if protname not in data.predictedSites:
                        data.predictedSites[ protname ] = {}

                    aa = l[2][0]
                    resid = int( l[1] )
                    score = round( float( l[3] ), 3)
                    isSignif = ("+" in l[5] )

                    if resid not in data.predictedSites[protname]:
                        data.predictedSites[protname][resid] = []

                    data.predictedSites[protname][resid].append({
                        "seq": aa,
                        "start": resid,
                        "end": resid,
                        "isSignif" : isSignif,
                        "score" : score,
                        "type": "N-Glyc",
                        "predictor": "netnglyc"
                    })


        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return data


