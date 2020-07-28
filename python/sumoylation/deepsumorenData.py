from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import os, sys

@dataclass
class deepsumoRenData:
    """Class that parses deepsumo_ren prediction output data.

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
            type : SUMO/SIM site
            cutoff: applied cutoff


    Public Methods
    --------------
    parse( outputFile : path ) -> deepsumoRenData
        Parses the deepsumo_ren prediction output file and add the data inside the
        above attribute data structure.

    """

    predictedSites : dict = field(default_factory=dict)

    @staticmethod
    def parse(outputFile: Path) -> deepsumoRenData :

        data = deepsumoRenData()

        try:
            f = open(outputFile, 'r')

            lines = f.readlines()
            for line in lines:
                l = line.split()
                if l[0] != "ID" :
                    protname = l[0]
                    if protname not in data.predictedSites:
                        data.predictedSites[ protname ] = []

                    seq = l[3]

                    pos = l[1].split('-')
                    start = int(pos[0])
                    end = int(pos[-1])

                    score = round( float( l[5] ), 3)
                    cutoff = round( float( l[6] ), 3)

                    isSignif = (score >= cutoff)

                    type = "SUMO" if l[7] == "SUMOylation" else "SIM"

                    data.predictedSites[ protname ].append( {
                        "seq": seq,
                        "start": start,
                        "end": end,
                        "isSignif" : isSignif,
                        "score" : score,
                        "cutoff" : cutoff,
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
# outputFile = CSW_HOME + "/test/cwl/modules/sumoylation/deepsumo_ren/expected_output/ex2.deepsumo_ren.out"
# test = deepsumoRenData.parse( outputFile )
