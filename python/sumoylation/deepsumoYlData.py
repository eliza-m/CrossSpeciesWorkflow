from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import os, sys

@dataclass
class deepsumoYlData:
    """Class that parses deepsumo_yl prediction output data.

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

        # Predictor specific
            type : SUMO/SIM site (only SUMO sites for this predictor)



    Public Methods
    --------------
    parse( outputFile : path ) -> deepsumoYlData
        Parses the deepsumo_yl prediction output file and add the data inside the
        above attribute data structure.

    """

    predictedSites : dict = field(default_factory=dict)

    @staticmethod
    def parse(outputFile: Path) -> deepsumoYlData :

        data = deepsumoYlData()

        try:
            f = open(outputFile, 'r')

            lines = f.readlines()
            for line in lines:
                l = line.split(',')
                if l[0] != 'Fragments name' :
                    # workaround because it concatenates protname and resid
                    header = l[0]
                    temp = header.split(' ')
                    if len(temp) == 2:
                        protname = temp[0][1:]
                        aa = temp[1][0]
                        pos = int( temp[1][1:])
                    else :
                        temp = header.split('K')
                        protname = temp[0][1:]
                        aa = "K"
                        pos = int( temp[1] )


                    protname = l[0].split(' ')[0][1:]
                    if protname not in data.predictedSites:
                        data.predictedSites[ protname ] = []

                    score = round( float( l[2] ), 3)

                    # only significant results are shown by this predictor
                    isSignif = True

                    # only SUMO sites are predicted
                    type = "SUMO"

                    data.predictedSites[ protname ].append( {
                        "seq": aa,
                        "start": pos,
                        "end": pos,
                        "isSignif" : isSignif,
                        "score" : score,
                        "type": type
                    } )


        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return data


# CSW_HOME = os.environ.get('CSW_HOME')
# outputFile = CSW_HOME + "/test/cwl/modules/sumoylation/deepsumo_yl/expected_output/ex1.deepsumo_yl.out"
# test = deepsumoYlData.parse( outputFile )
