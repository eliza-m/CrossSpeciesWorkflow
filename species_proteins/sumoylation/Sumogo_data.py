from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import sys, re
import requests
from time import sleep
from bs4 import BeautifulSoup as bs


@dataclass
class Sumogo_data:
    """Class that parses SUMOgo prediction output data.

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
            type : string (C-glyc)
            predictor : string (for cases where multiple predictors are available)

    Public Methods
    --------------
    parse( outputfile : path ) -> Gpspail_data
        Parses the GpsPail prediction output file and add the data inside the
        above attribute data structure.

    submit_online (fastafile : Path, outputfile: Path)
        Submits online job. Provided as arguments are the input fasta file and the
        prediction output file paths
H
    """

    predicted_sites: dict

    @staticmethod
    def parse(outputfile: Path) -> Sumogo_data:

        predicted_sites = {}

        try:
            with open(outputfile, 'r', encoding='utf-8') as f:
                content = f.read()
                soup = bs(content, "html.parser")
                table = soup.find('table')
                rows = table.findAll('tr')

                protname = (outputfile.name).split('.')[0]
                type = 'SUMO'

                for r in rows:
                    cols = r.findAll('td')
                    # in very few cases, without a clear reason some resids are not shown and columns are shifted...
                    # therefore we introduce a list of conditions for parsing
                    if len(cols) == 2 and cols[0].text and cols[1].text and cols[0].text != 'Position':
                        resid = int(cols[0].text)
                        score = round(float(cols[1].text), 3)
                        is_signif = score >= 0.5

                        if protname not in predicted_sites:
                            predicted_sites[protname] = {}
                        if resid not in predicted_sites[protname]:
                            predicted_sites[protname][resid] = []

                        predicted_sites[protname][resid].append({
                            "seq": '',
                            "start": resid,
                            "end": resid,
                            "is_signif": is_signif,
                            "score": score,
                            "type": type,
                            "predictor": "sumogo_online"
                        })

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return Sumogo_data(predicted_sites)

    @staticmethod
    def submit_online(fastafile: Path, outputfile: Path):

        try:
            # launch job
            url = 'http://predictor.nchu.edu.tw/SUMOgo/result.php'

            with open(fastafile, 'r') as f:
                seq = f.read()

            data = { 'seq': seq }
            s = requests.Session()
            r1 = s.post(url, data=data)

            #retrieve results
            temp = re.search(r"JOBID:.+is", r1.text)
            jobid = temp.group().split(':')[1].split(' ')[0][0:-1]

            sleep(2)
            r2 = s.post(url, data={'jid': jobid })
            while "is being processed" in r2.text:
                sleep(2)
                r2 = s.post(url, data={'jid': jobid })

            r2.raise_for_status()

            # html archive
            with open(outputfile, 'w', encoding='utf-8') as f:
                f.write(r2.text)

        except Exception as e:
            print("Failed: Online job submission failed !!!!")
            if hasattr(e, 'message'): print(e.message)
            else: print(e)
            with open(outputfile, 'w', encoding='utf-8') as f:
                print("#Failed: Online job submission failed !!!! Error: ", e, file=f)
            pass


