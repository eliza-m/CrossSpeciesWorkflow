from __future__ import annotations
from typing import *
from dataclasses import dataclass, field
from pathlib import Path
import os, sys
import requests
import re
from time import sleep


@dataclass
class Netnglyc_data:
    """Class that parses NetNglyc prediction output data.

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
    parse( outputfile : path ) -> NetNglyc_data
        Parses the NetNglyc prediction output file and add the data inside the
        above attribute data structure.

    submit_online (fastafile : Path, outputfile: Path)
        Submits online job. Provided as arguments are the input fasta file and the
        prediction output file paths

    """

    predicted_sites : dict

    @staticmethod
    def parse(outputfile: Path) -> Netnglyc_data :
        """Parses predictor's output"""

        predicted_sites = {}

        try:
            f = open(outputfile, 'r')

            lines = f.readlines()
            if "Failed: Online job submission failed" in lines[0]:
                protname = (outputfile.name).split('.')[0]
                predicted_sites[protname] = {}
                return Netnglyc_data(predicted_sites)

            if lines[0][0] == "<":
                predictor = "netnglyc:1.0_online"
            else : predictor = "netnglyc:1.0_local"

            for line in lines:
                l = line.split()
                if len(l) > 3 and l[0]== "Name:" :
                    protname = l[1]
                    if protname not in predicted_sites:
                        predicted_sites[ protname ] = {}

                if len(l) >= 6 and l[0] in predicted_sites and l[2][0]=="N":
                    protname = l[0]
                    aa = l[2][0]
                    resid = int( l[1] )
                    score = round( float( l[3] ), 3)
                    is_signif = ("+" in l[-1] )

                    if resid not in predicted_sites[protname]:
                        predicted_sites[protname][resid] = []

                    predicted_sites[protname][resid].append({
                        "seq": aa,
                        "start": resid,
                        "end": resid,
                        "is_signif" : is_signif,
                        "score" : score,
                        "type": "N-glyc",
                        "predictor": predictor
                    })


        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return Netnglyc_data(predicted_sites)


    @staticmethod
    def submit_online (fastafile : Path, outputfile: Path) :
        """Submits online job. Provided as arguments are the input fasta file and the
                prediction output filename"""

        try:
            url = 'https://services.healthtech.dtu.dk/cgi-bin/webface2.cgi'

            #launch job
            files = {'SEQSUB': open(fastafile, 'r')}
            data = {'configfile':'/var/www/html/services/NetNGlyc-1.0/webface.cf'}
            r1 = requests.post(url, data=data, files=files)

            #retrieve results
            temp = re.search(r"jobid: .+ status", r1.text)
            jobid = temp.group().split(' ')[1]

            sleep(2)
            r2 = requests.get(url, params={'jobid' : jobid })

            count = 0; maxtime = 300
            while jobid in r2.text and count < maxtime/2:
                sleep(2)
                r2 = requests.get(url, params={'jobid': jobid })
                count +=1

            r2.raise_for_status()

            file = open(outputfile, "w")
            file.write(r2.text)

        except Exception as e:
            print("Failed: Online job submission failed !!!!")
            if hasattr(e, 'message'): print(e.message)
            else: print(e)
            with open(outputfile, 'w', encoding='utf-8') as f:
                print("#Failed: Online job submission failed !!!! Error: ", e, file=f)
            pass

