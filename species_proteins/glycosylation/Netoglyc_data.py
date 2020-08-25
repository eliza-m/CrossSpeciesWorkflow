from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import os, sys
import requests
import re
from time import sleep

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

    submitOnline (fastaFile : Path, outputFile: Path)
        Submits online job. Provided as arguments are the input fasta file and the
        prediction output file paths

    """

    predictedSites : dict = field(default_factory=dict)



    @staticmethod
    def parse(outputFile: Path) -> NetOglycData:

        try:
            f = open(outputFile, 'r')

            lines = f.readlines()

            if lines[0][0] == "<":
                # online job output
                predictedSites = NetOglycData.__parseHTML( lines )

            else :
                # docker container output
                predictedSites = NetOglycData.__parseLocaloutput( lines )


        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return NetOglycData(predictedSites)



    @staticmethod
    def submitOnline (fastaFile : Path, outputFile: Path) :
        #  Only single protein fasta file !!!!!

        url = 'https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi'

        #launch job
        files = {'SEQSUB': open(fastaFile, 'r')}
        data = {'configfile':'/var/www/html/services/NetOGlyc-4.0/webface.cf'}
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



    @staticmethod
    def __parseLocaloutput(lines: list) -> dict :

        predictedSites = {}
        for line in lines:
            l = line.split()
            if len(l) == 7:
                if l[0] == 'Name':
                    header = l
                else:
                    protname = l[0]
                    if protname not in predictedSites:
                        predictedSites[protname] = {}

                    aa = l[1]
                    resid = int(l[2])
                    gscore = round(float(l[2]), 3)
                    iscore = round(float(l[3]), 3)
                    isSignif = (l[5] != ".")

                    if resid not in predictedSites[protname]:
                        predictedSites[protname][resid] = []

                    predictedSites[protname][resid].append({
                        "seq": aa,
                        "start": resid,
                        "end": resid,
                        "isSignif": isSignif,
                        "score": gscore,
                        "iscore": iscore,
                        "type": "O-GalNAc",
                        "predictor": "netoglyc:3.1_local",
                    })

        return predictedSites


    @staticmethod
    def __parseHTML(lines: list) -> dict :

        predictedSites = {}
        for line in lines:
            l = line.split()
            if len(l) in [8, 9] and l[0][0] not in [ "#", "<" ]:
                protname = l[0]
                if protname not in predictedSites:
                    predictedSites[protname] = {}

                # not shown in v4 output
                aa = ""
                start = int(l[3])
                end = int(l[4])
                score = round(float(l[5]), 3)
                isSignif = ( len(l) ==9 and l[8] == "#POSITIVE" )

                resid = start
                if resid not in predictedSites[protname]:
                    predictedSites[protname][resid] = []

                predictedSites[protname][resid].append({
                    "seq": aa,
                    "start": start,
                    "end": end,
                    "isSignif": isSignif,
                    "score": score,
                    "type": "O-linked",
                    "predictor": "netoglyc:4.0_online",
                })


        return predictedSites


