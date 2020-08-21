from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import os, sys
import requests
import re
from time import sleep
from bs4 import BeautifulSoup as bs

@dataclass
class NGlyDEData:
    """Class that parses NGlyDE prediction output data.

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
    parse( outputFile : path ) -> NGlyDE
        Parses the prediction output file and add the data inside the
        above attribute data structure.

    submitOnline (fastaFile : Path, outputFile: Path)
        Submits online job. Provided as arguments are the input fasta file and the
        prediction output file paths

    """

    predictedSites : dict

    @staticmethod
    def parse(outputFile: Path) -> NGlyDE :

        predictedSites = {}

        try:
            f = open(outputFile, 'r')

            # unfortunatelyy the output does not contain the </*> closing markups to be
            # easilly parsed...we found a simpler approach

            content = f.read()

            content = content.replace( "</tr><th>", "</tr><tr><th>" )
            content = content.replace("</tr>", "</th></tr>")
            content = re.sub('([\d])<th>', r'\1</th><th>', content)

            soup = bs(content, "html.parser")
            rows = soup.findAll('tr')

            for r in range( 1, len(rows) ):
                cols = rows[r].findAll('th')
                i = 0;
                if len(cols) == 4:
                    # new proteinname
                    i=1;
                    protname = cols[0].text.split()[0]
                    if protname not in predictedSites:
                        predictedSites[protname] = {}

                if cols[i+1].content != '.':
                    aa = ''  # not shown in input
                    # because text variable is bogous due to missing tags
                    resid = int(cols[i].text)
                    score = round(float(cols[i+1].text), 3)
                    isSignif = ("Yes" in cols[i+2].text)

                    if resid not in predictedSites[protname]:
                        predictedSites[protname][resid] = []

                    predictedSites[protname][resid].append({
                        "seq": aa,
                        "start": resid,
                        "end": resid,
                        "isSignif": isSignif,
                        "score": score,
                        "type": "N-linked",
                        "predictor": "NGlyDE_online"
                    })

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return NGlyDEData(predictedSites)


    @staticmethod
    def submitOnline (fastaFile : Path, outputFile: Path) :

        url1 = 'http://bioapp.iis.sinica.edu.tw/Nglyde/run.php'
        url2 = 'http://bioapp.iis.sinica.edu.tw/GlycoPred/MakeSummary.php'
        message = "All queries have been done!!"

        #launch job
        with open(fastaFile, 'r') as f :
            seq = f.read()

        data = {'sequence': seq}
        r1 = requests.post(url1, data=data )


        #retrieve results
        temp = re.search(r"job=.+\)", r1.text)
        jobid = temp.group().split('=')[1][:-1]

        sleep(2)
        r2 = requests.get(url2, params={'job' : jobid })

        while message not in r2.text:
            sleep(2)
            r2 = requests.get(url2, params={'job': jobid })

        r2.raise_for_status()

        file = open(outputFile, "w")
        file.write(r2.text)

