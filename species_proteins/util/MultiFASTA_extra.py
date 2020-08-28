from bioservices.apps import FASTA, MultiFASTA
from pathlib import Path
import sys


class MultiFASTA_extra(MultiFASTA):
    """
		Inherits bioservices.apps.MultiFASTA and introduces additional features
    """

    def read_fasta(self, filename):
    # Temporary fix for bioservices MultiFASTA read_fasta funtion
    # that recognises only particular headers such as Swissprot(sp) but not Trembl (tr) part of Uniprot...
    # by overriding the read_fasta function -> see bellow (at the end)

        """Load several FASTA from a filename"""
        fh = open(filename, "r")
        data = fh.read()
        fh.close()

        # we split according to ">2 character
        for thisfasta in data.split(">")[1:]:
            f = FASTA()
            f._fasta = f._interpret(thisfasta)

            # temporary fix for header recognition
            if f.accession == None :
                if thisfasta[0:3] == 'tr|':
                    thisfasta = 'sp|' + thisfasta[3:]
                if '|' not in thisfasta:
                    temp = thisfasta.split('\n')
                    newheader = 'sp|' + temp[0].split()[0] + '|blabla\n'
                    seq = ''
                    for l in range( 1, len(temp) ):
                        seq = seq + temp[l]
                    thisfasta = newheader + seq
                f._fasta = f._interpret(thisfasta)


            if f.accession != None and f.accession not in self.ids:
                self._fasta[f.accession] = f
            else:
                print("Accession %s is already in the ids list or could not be interpreted. skipped" % str(
                    f.accession))


