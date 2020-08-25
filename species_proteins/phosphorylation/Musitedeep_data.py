from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import os, sys

@dataclass
class Musitedeep_data:
    """Class that parses Musitedeep prediction output data.

    Parameters
    ----------

    Attributes
    ----------
    predicted_sites : Dictionary
        predicted_sites [ protein name ][ start resid ] : array of entry dict
        entry dict has the following keys:

        # Common to all PTS predictors
            seq : string (stretch of the predicted sequence)
            start : starting residue id
            end : ending residue id
            is_signif : bool (is the method's specific scoring indicating a
                            potentially significant result)
            score : float (probability)
            type : string (generic or a specific kinase)
            predictor : string (for cases where multiple predictors are available)

    Public Methods
    --------------
    parse( outputfile : path ) -> Musitedeep_data
        Parses the Musitedeep prediction output file and add the data inside the
        above attribute data structure.

    """

    predicted_sites : dict

    @staticmethod
    def parse(outputfile: Path) -> Musitedeep_data :

        predicted_sites={}

        try:
            f = open(outputfile, 'r')

            enzyme = ''
            if 'general' in outputfile.name:
                enzyme = 'general'
            else:
                for e in ['CDK', 'PKA', 'CK2', 'MAPK' or 'PKC']:
                    if e in outputfile.name:
                        enzyme = e

            lines = f.readlines()
            for line in lines:
                l = line.split('\t')
                if len(l) == 4  :

                    protname = l[0].split(' ')[0][2:]
                    if protname not in predicted_sites:
                        predicted_sites[protname] = {}

                    aa = l[2].split('"')[1]
                    resid = int(l[1])
                    score = round(float(l[3]), 3)

                    is_signif = (score >= 0.5)

                    if resid not in predicted_sites[protname]:
                        predicted_sites[protname][resid] = []

                    predicted_sites[protname][resid].append({
                        "seq": aa,
                        "start": resid,
                        "end": resid,
                        "is_signif": is_signif,
                        "score": score,
                        "type": aa + "-phosph",
                        "enzyme": enzyme,
                        "predictor": "musitedeep"
                    })


        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return Musitedeep_data(predicted_sites)


