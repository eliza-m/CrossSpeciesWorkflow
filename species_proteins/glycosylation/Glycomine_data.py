from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import sys
import requests
from bs4 import BeautifulSoup as bs

@dataclass
class Glycomine_data:
    """Class that parses Glycomine prediction output data.

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
            score : float (interpretation differs between methods)
            type : string (N-glyc)
            predictor : string (for cases where multiple predictors are available)

    Public Methods
    --------------
    parse( outputfile : path ) -> Glycomine_data
        Parses the Glycomine prediction output file and add the data inside the
        above attribute data structure.

    submit_online (fastafile : Path, outputfile: Path, type: str)
        Submits online job. Provided as arguments are the input fasta file and the
        prediction output file paths
        Type: 'N', 'C', 'O' indicates the glycosylation type to be predicted

    """

    predicted_sites : dict

    @staticmethod
    def parse(outputfile: Path) -> Glycomine_data :
        """Parses predictor's output"""

        predicted_sites = {}

        try:
            f = open(outputfile, 'r')

            if "Failed: Online job submission failed" in f.read():
                protname = (outputfile.name).split('.')[0]
                predicted_sites = {}
                predicted_sites[protname] = {}
                return Glycomine_data(predicted_sites)

            soup = bs(f, "html.parser")

            h = soup.find('h2')
            protname = h.contents[0].split()[0][1:]
            if protname not in predicted_sites:
                predicted_sites[ protname ] = {}

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
                    is_signif = (score >= 0.5)
                elif c % 6 == 5:
                    type = val[0] + '-glyc'

                    if resid not in predicted_sites[protname]:
                        predicted_sites[protname][resid] = []

                    predicted_sites[protname][resid].append({
                        "seq": aa,
                        "start": resid,
                        "end": resid,
                        "is_signif" : is_signif,
                        "score" : score,
                        "type" : type,
                        "predictor": "Glycomine_online"
                    })


        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return Glycomine_data(predicted_sites)


    @staticmethod
    def submit_online (fastafile : Path, outputfile: Path, type: str) :
        """Submits online job. Provided as arguments are the input fasta file and the
                prediction output filename"""

        try:
            if type not in "NOC":
                print("Type should be one of the following: 'N', 'C' or 'O'")
                raise

            url = 'http://glycomine.erc.monash.edu/Lab/GlycoMine/GlycoMine.pl'

            #launch job & retrieve results
            with open(fastafile, 'r') as f :
                seq = f.read()

            data = {'txtInput':seq, 'specie':type }
            r = requests.post(url, data=data)

            r.raise_for_status()
            file = open(outputfile, "w")
            file.write(r.text)

        except Exception as e:
            print("Failed: Online job submission failed !!!!")
            if hasattr(e, 'message'): print(e.message)
            else: print(e)
            with open(outputfile, 'w', encoding='utf-8') as f:
                print("#Failed: Online job submission failed !!!! Error: ", e, file=f)
            pass