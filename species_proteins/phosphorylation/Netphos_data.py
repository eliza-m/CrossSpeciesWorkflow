from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import sys
import re
import requests
from time import sleep

@dataclass
class Netphos_data:
    """Class that parses Netphos prediction output data.

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
            score : float (probability)
            type : string (generic or a specific kinase)
            predictor : string (for cases where multiple predictors are available)

    Public Methods
    --------------
    parse( outputfile : path ) -> Netphos
        Parses the Netphos prediction output file and add the data inside the
        above attribute data structure.

    """

    predicted_sites : dict


    @staticmethod
    def parse(outputfile: Path) -> Netphos_data:

        try:
            f = open(outputfile, 'r')

            lines = f.readlines()

            if lines[0][0] == "<":
                # online job output
                predicted_sites = Netphos_data.__parse_html(lines)

            else :
                # docker container output
                predicted_sites = Netphos_data.__parse_localoutput(lines)


        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return Netphos_data(predicted_sites)




    @staticmethod
    def submit_online (fastafile : Path, outputfile: Path) :
        #  Only single protein fasta file !!!!!

        try:
            url = 'https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi'

            #launch job
            files = {'SEQSUB': open(fastafile, 'r')}
            data = {'configfile':'/var/www/html/services/NetPhos-3.1/webface.cf'}
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
                protname = l[0]
                if protname not in predicted_sites:
                    predicted_sites[protname] = {}

                aa = l[1]
                resid = int(l[3])
                score = round(float(l[4]), 3)
                is_signif = (score >= 0.5)
                enzyme = l[6]

                if resid not in predicted_sites[protname]:
                    predicted_sites[protname][resid] = []

                predicted_sites[protname][resid].append({
                    "seq": aa,
                    "start": resid,
                    "end": resid,
                    "is_signif": is_signif,
                    "score": score,
                    "type" : aa + "-phosph",
                    "enzyme": enzyme,
                    "predictor": "netphos:3.1_local"
                })

        return predicted_sites


    @staticmethod
    def __parse_html(lines: list) -> dict :

        predicted_sites = {}
        for line in lines:
            l = line.split()
            if len(l) == 8 and l[0] == '#' and l[1] != 'Sequence':
                protname = l[1]
                if protname not in predicted_sites:
                    predicted_sites[protname] = {}

                aa = l[3]
                resid = int(l[2])
                score = round(float(l[5]), 3)
                enzyme = l[6]
                is_signif = ( l[7] == "YES" )

                if resid not in predicted_sites[protname]:
                    predicted_sites[protname][resid] = []

                predicted_sites[protname][resid].append({
                    "seq": aa,
                    "start": resid,
                    "end": resid,
                    "is_signif": is_signif,
                    "score": score,
                    "type": aa + "-phosph",
                    "enzyme": enzyme,
                    "predictor": "netphos:3.1_online",
                })

        return predicted_sites




