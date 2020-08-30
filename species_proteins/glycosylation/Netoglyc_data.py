from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import os, sys
import requests
import re
from time import sleep

@dataclass
class Netoglyc_data:
    """Class that parses NetOglyc prediction output data.

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
            score : float (interpretation differs between methods)
            type : string (O-glyc)
            predictor : string (for cases where multiple predictors are available)

        # Predictor specific
            iscore : float
            comment : string


    Public Methods
    --------------
    parse( outputfile : path ) -> NetOglyc
        Parses the NetOglyc prediction output file and add the data inside the
        above attribute data structure.

    submit_online (fastafile : Path, outputfile: Path)
        Submits online job. Provided as arguments are the input fasta file and the
        prediction output file paths

    """

    predicted_sites : dict = field(default_factory=dict)



    @staticmethod
    def parse(outputfile: Path) -> Netoglyc_data:

        try:
            f = open(outputfile, 'r')

            lines = f.readlines()

            if lines[0][0] == "<":
                # online job output
                predicted_sites = Netoglyc_data.__parse_html(lines)

            else :
                # docker container output
                predicted_sites = Netoglyc_data.__parse_localoutput(lines)


        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return Netoglyc_data(predicted_sites)



    @staticmethod
    def submit_online (fastafile : Path, outputfile: Path) :
        #  Only single protein fasta file !!!!!

        try:
            url = 'https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi'

            #launch job
            files = {'SEQSUB': open(fastafile, 'r')}
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

            file = open(outputfile, "w")
            file.write(r2.text)

        except Exception as e:
            print("Failed: Online job submission failed !!!!")
            if hasattr(e, 'message'): print(e.message)
            else: print(e)
            pass




    @staticmethod
    def __parse_localoutput(lines: list) -> dict :

        predicted_sites = {}
        for line in lines:
            l = line.split()
            if len(l) == 7:
                if l[0] == 'Name':
                    header = l
                else:
                    protname = l[0]
                    if protname not in predicted_sites:
                        predicted_sites[protname] = {}

                    aa = l[1]
                    resid = int(l[2])
                    gscore = round(float(l[2]), 3)
                    iscore = round(float(l[3]), 3)
                    is_signif = (l[5] != ".")

                    if resid not in predicted_sites[protname]:
                        predicted_sites[protname][resid] = []

                    predicted_sites[protname][resid].append({
                        "seq": aa,
                        "start": resid,
                        "end": resid,
                        "is_signif": is_signif,
                        "score": gscore,
                        "iscore": iscore,
                        "type": "O-glyc",
                        "predictor": "netoglyc:3.1_local",
                    })

        return predicted_sites


    @staticmethod
    def __parse_html(lines: list) -> dict :

        predicted_sites = {}
        for line in lines:
            l = line.split()
            if len(l) in [8, 9] and l[0][0] not in [ "#", "<" ]:
                protname = l[0]
                if protname not in predicted_sites:
                    predicted_sites[protname] = {}

                # not shown in v4 output
                aa = ""
                start = int(l[3])
                end = int(l[4])
                score = round(float(l[5]), 3)
                is_signif = ( len(l) ==9 and l[8] == "#POSITIVE" )

                resid = start
                if resid not in predicted_sites[protname]:
                    predicted_sites[protname][resid] = []

                predicted_sites[protname][resid].append({
                    "seq": aa,
                    "start": start,
                    "end": end,
                    "is_signif": is_signif,
                    "score": score,
                    "type": "O-glyc",
                    "predictor": "netoglyc:4.0_online",
                })


        return predicted_sites


