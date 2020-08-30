from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import sys
import requests
from bs4 import BeautifulSoup as bs


@dataclass
class Gpspail_data:
    """Class that parses GpsPail prediction output data.

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
    enzymes = ['CREBBP', 'EP300', 'HAT1', 'KAT2A', 'KAT2B', 'KAT5', 'KAT8']

    @staticmethod
    def parse(outputfile: Path) -> Gpspail_data:

        predicted_sites = {}

        try:
            with open(outputfile, 'r', encoding='utf-8') as f:
                content = f.read()
                soup = bs(content, "html.parser")
                table = soup.find('tbody')
                rows = table.findAll('tr')

                for r in rows:
                    cols = r.findAll('td')
                    protname = cols[0].text.split()[0]
                    resid = int(cols[1].text)
                    aa = cols[2].text[8]
                    enzyme = cols[3].text.split()[0]
                    score = round(float(cols[4].text), 3)
                    cutoff = round(float(cols[5].text), 3)

                    is_signif = score >= cutoff

                    if protname not in predicted_sites:
                        predicted_sites[protname] = {}

                    if resid not in predicted_sites[protname]:
                        predicted_sites[protname][resid] = []

                    predicted_sites[protname][resid].append({
                        "seq": aa,
                        "start": resid,
                        "end": resid,
                        "is_signif": is_signif,
                        "score": score,
                        "cutoff": cutoff,
                        "type": "K-acet",
                        "enzyme": enzyme,
                        "predictor": "gpspail:2.0_online"
                    })

        except OSError as e:
            print("File error:", sys.exc_info()[0])
            raise

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return Gpspail_data(predicted_sites)

    @staticmethod
    def submit_online(fastafile: Path, outputfile: Path):

        try:
            url1 = 'http://pail.biocuckoo.org/webcomp/convert.php'
            url2 = 'http://pail.biocuckoo.org/wsresult.php'
            url3 = 'http://pail.biocuckoo.org/webcomp/download.php'

            # launch job

            with open(fastafile, 'r') as f:
                seq = f.read()
                if "\r\n" not in seq:
                    seq = seq.replace("\n", "\r\n")

            data = {'tag': 'on', 'MAX_FILE_SIZE': '20M',
                    'Fasta_Input': seq,
                    'threhold': 'Medium',
                    'All': 'CREBBP;EP300;HAT1;KAT2A;KAT2B;KAT5;KAT8',
                    'CREBBP': 'CREBBP',
                    'EP300': 'EP300',
                    'HAT1': 'HAT1',
                    'KAT2A': 'KAT2A',
                    'KAT2B': 'KAT2B',
                    'KAT5': 'KAT5',
                    'KAT8': 'KAT8'
                    }

            s = requests.Session()
            r1 = s.post(url1, data=data)

            # retrieve results
            r2 = s.get(url2)
            r2.raise_for_status()

            r3 = s.post(url3)
            r3.raise_for_status()

            # html archive
            with open(outputfile, 'w', encoding='utf-8') as f:
                f.write(r2.text)

            # # zip archive
            # # zipfile = (outputfile.stem + '_raw').with_suffix('.zip')
            # zipfile = outputfile.split('.')[0] + 'gpspail_raw.zip'
            # with open(zipfile, 'wb') as f:
            #     f.write(r3.content)

        except Exception as e:
            print("Failed: Online job submission failed !!!!")
            if hasattr(e, 'message'): print(e.message)
            else: print(e)
            pass