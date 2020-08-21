from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import sys
import requests
from bs4 import BeautifulSoup as bs

@dataclass
class GlycomineData:
    """Class that parses Glycomine prediction output data.

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
        Parses the Glycomine prediction output file and add the data inside the
        above attribute data structure.

    submitOnline (fastaFile : Path, outputFile: Path, type: str)
        Submits online job. Provided as arguments are the input fasta file and the
        prediction output file paths
        Type: 'N', 'C', 'O' indicates the glycosylation type to be predicted

    """

    predictedSites : dict

    @staticmethod
    def parse(outputFile: Path) -> GlycomineData :

        predictedSites = {}

        try:
            f = open(outputFile, 'r')
            soup = bs(f, "html.parser")

            h = soup.find('h2')
            protname = h.contents[0].split()[0][1:]
            if protname not in predictedSites:
                predictedSites[ protname ] = {}

            table = soup.find("tbody")

            # rows are not well separated....
            cols = table.findAll('td')
            for c in range( len(cols) ) :
                val = cols[c].text
                if c % 6 == 1:
                    resid = int(val)
                elif c % 6 == 2:
                    aa = val
                elif c % 6 == 4:
                    score = float(val)
                    isSignif = (score >= 0.5)
                elif c % 6 == 5:
                    type = val

                    if resid not in predictedSites[protname]:
                        predictedSites[protname][resid] = {}
                        predictedSites[protname][resid][type] = []

                    predictedSites[protname][resid].append({
                        "seq": aa,
                        "start": resid,
                        "end": resid,
                        "isSignif" : isSignif,
                        "score" : score,
                        "predictor": "Glycomine_online"
                    })


        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return GlycomineData(predictedSites)


    @staticmethod
    def submitOnline (fastaFile : Path, outputFile: Path, type: str) :

        if type not in "NOC":
            print("Type should be one of the following: 'N', 'C' or 'O'")
            raise

        url = 'http://glycomine.erc.monash.edu/Lab/GlycoMine/GlycoMine.pl'

        #launch job & retrieve results
        with open(fastaFile, 'r') as f :
            seq = f.read()

        data = {'txtInput':seq, 'specie':type }
        r = requests.post(url, data=data)

        r.raise_for_status()
        file = open(outputFile, "w")
        file.write(r.text)

