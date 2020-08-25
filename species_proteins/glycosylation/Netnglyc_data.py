from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import os, sys
import requests
import re
from time import sleep


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

    submitOnline (fastaFile : Path, outputFile: Path)
        Submits online job. Provided as arguments are the input fasta file and the
        prediction output file paths

    """

    predictedSites : dict

    @staticmethod
    def parse(outputFile: Path) -> NetNglycData :

        predictedSites = {}

        try:
            f = open(outputFile, 'r')

            lines = f.readlines()

            if lines[0][0] == "<":
                predictor = "netnglyc:1.0_online"
            else : predictor = "netnglyc:1.0_local"

            for line in lines:
                l = line.split()
                if len(l) > 3 and l[0]== "Name:" :
                    protname = l[1]
                    if protname not in predictedSites:
                        predictedSites[ protname ] = {}

                if len(l) >= 6 and l[0] in predictedSites and l[2][0]=="N":
                    protname = l[0]
                    aa = l[2][0]
                    resid = int( l[1] )
                    score = round( float( l[3] ), 3)
                    isSignif = ("+" in l[-1] )

                    if resid not in predictedSites[protname]:
                        predictedSites[protname][resid] = []

                    predictedSites[protname][resid].append({
                        "seq": aa,
                        "start": resid,
                        "end": resid,
                        "isSignif" : isSignif,
                        "score" : score,
                        "type": "N-linked",
                        "predictor": predictor
                    })


        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return NetNglycData(predictedSites)


    @staticmethod
    def submitOnline (fastaFile : Path, outputFile: Path) :

        url = 'https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi'

        #launch job
        files = {'SEQSUB': open(fastaFile, 'r')}
        data = {'configfile':'/var/www/html/services/NetNGlyc-1.0/webface.cf'}
        r1 = requests.post(url, data=data, files=files)

        #retrieve results
        temp = re.search(r"jobid: .+ status", r1.text)
        jobid = temp.group().split(' ')[1]

        sleep(2)
        r2 = requests.get(url, params={'jobid' : jobid })

        while jobid in r2.text:
            sleep(2)
            r2 = requests.get(url, params={'jobid': jobid })


        r2.raise_for_status()

        file = open(outputFile, "w")
        file.write(r2.text)


