from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import os, sys

@dataclass
class IsoglypData:
    """Class that parses Isoglyp prediction output data.

    Parameters
    ----------

    Attributes
    ----------
    predictedSites : Dictionary
        predictedSites [ protein name ][ site ] [ entry dict ]
        entry dict has the following keys:

        # Common to all PTS predictors :
            seq : string (stretch of the predicted sequence)
            start : starting residue id
            end : ending residue id
            isSignif : bool (is the method's specific scoring indicating a
                            potentially significant result)
            score : maximum EVP from all isoforms

        # Predictor specific :
            T1: EVP value for T1 isoform
            ...
            Tn: EVP value for Tn isoform


    Public Methods
    --------------
    parse( outputFile : path ) -> IsoglypData
        Parses the Isoglyp prediction output file and add the data inside the
        above attribute data structure.

    """

    predictedSites : dict = field(default_factory=dict)

    @staticmethod
    def parse(outputFile: Path) -> IsoglypData :

        data = IsoglypData()

        try:
            f = open(outputFile, 'r')

            lines = f.readlines()
            for line in lines:
                l = line.split(',')
                if len(l) > 1 and l[0][0] != '#' :

                    if l[0] == 'Sequence Name':
                        header = l
                    else:
                        protname = l[0].split()[0][1:]
                        if protname not in data.predictedSites:
                            data.predictedSites[ protname ] = []

                        aa = l[1]
                        resid = int( l[2] )
                        max = round( float( l[-1] ), 3)
                        isSignif = (max >= 1)

                        data.predictedSites[ protname ].append( {
                            "aa": aa,
                            "resid": resid,
                            "score" : max,
                            "isSignif" : isSignif
                        } )

                        # add EVP (enhancement value product) values for each
                        # of the predicted isoformes (T1...Tn). Read more about
                        # this in their documentation
                        for it in range(6, len(header) ):
                            if header[it][0] == "T":
                                key = header[it]
                                value = round( float(l[it]), 4 )
                                data.predictedSites[protname][-1][key] = value


        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return data



# CSW_HOME = os.environ.get('CSW_HOME')
# outputFile = CSW_HOME + "/test/bash/single_protein/output/glycosylation/isoglyp/expected_output/1pazA.isoglyp.out"
# test = IsoglypData.parse( outputFile )
# print(test.predictedSites)
