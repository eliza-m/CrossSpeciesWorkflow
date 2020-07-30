from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import os, sys

@dataclass
class NetOglycData:
    """Class that parses NetOglyc prediction output data.

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
            type : string (O-glyc)
            predictor : string (for cases where multiple predictors are available)

        # Predictor specific
            iscore : float
            comment : string


    Public Methods
    --------------
    parse( outputFile : path ) -> NetOglyc
        Parses the NetOglyc prediction output file and add the data inside the
        above attribute data structure.

    """

    predictedSites : dict = field(default_factory=dict)

    @staticmethod
    def parse(outputFile: Path) -> NetOglycData :

        data = NetOglycData()

        try:
            f = open(outputFile, 'r')

            lines = f.readlines()
            for line in lines:
                l = line.split()
                if len(l) == 7 :
                    if l[0] == 'Name':
                        header = l
                    else:
                        protname = l[0]
                        if protname not in data.predictedSites:
                            data.predictedSites[ protname ] = {}

                        aa = l[1]
                        resid = int( l[2] )
                        gscore = round( float( l[2] ), 3)
                        iscore = round( float( l[3] ), 3)
                        isSignif = (l[5] != ".")
                        comment = l[6]

                        if resid not in data.predictedSites[protname]:
                            data.predictedSites[protname][resid] = []

                        data.predictedSites[protname][resid].append({
                            "seq": aa,
                            "start": resid,
                            "end": resid,
                            "isSignif" : isSignif,
                            "score" : gscore,
                            "iscore" : iscore,
                            "type": "O-Glyc",
                            "predictor": "netoglyc",
                            "comment" : comment
                        } )

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return data


