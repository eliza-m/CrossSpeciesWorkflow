from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import sys

@dataclass
class Isoglyp_data:
    """Class that parses Isoglyp prediction output data.

    Attributes
    ----------
    predicted_sites : Dictionary
        predicted_sites [ protein name ][ start resid ] : array of entry dict
        entry dict has the following keys:

        # Common to all PTS predictors :
            seq : string (stretch of the predicted sequence)
            start : starting residue id
            end : ending residue id
            is_signif : bool (is the method's specific scoring indicating a
                            potentially significant result)
            score : maximum EVP from all isoforms
            type : string (O-glyc)
            predictor : string (for cases where multiple predictors are available)

        # Predictor specific :
            T1: EVP value for T1 isoform
            ...
            Tn: EVP value for Tn isoform


    Public Methods
    --------------
    parse( outputfile : path ) -> Isoglyp_data
        Parses the Isoglyp prediction output file and add the data inside the
        above attribute data structure.

    """

    predicted_sites : dict

    @staticmethod
    def parse(outputfile: Path) -> Isoglyp_data :
        """Parses predictor's output"""

        predicted_sites = {}
        try:
            f = open(outputfile, 'r')

            lines = f.readlines()
            for line in lines:
                l = line.split(',')
                if len(l) > 1 and l[0][0] != '#' :

                    if l[0] == 'Sequence Name':
                        header = l
                    else:
                        protname = l[0].split()[0][1:]
                        if protname not in predicted_sites:
                            predicted_sites[ protname ] = {}

                        aa = l[1]
                        resid = int( l[2] )
                        max = round( float( l[-1] ), 3)
                        is_signif = (max >= 1)

                        if resid not in predicted_sites[protname]:
                            predicted_sites[protname][resid] = []

                        predicted_sites[protname][resid].append({
                            "seq": aa,
                            "start": resid,
                            "end": resid,
                            "score" : max,
                            "is_signif" : is_signif,
                            "type": "O-glyc",
                            "predictor": "isoglyp_local"
                        })

                        # add EVP (enhancement value product) values for each
                        # of the predicted isoformes (T1...Tn). Read more about
                        # this in their documentation
                        for it in range(6, len(header) ):
                            if header[it][0] == "T":
                                key = header[it]
                                value = round( float(l[it]), 4 )
                                predicted_sites[protname][resid][-1][key] = value


        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return Isoglyp_data(predicted_sites)
