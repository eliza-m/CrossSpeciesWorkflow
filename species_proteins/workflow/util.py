from bioservices.apps import FASTA, MultiFASTA
from pathlib import Path
import sys

def map_aln( alnfile : Path ) -> dict:

    # Temporary fix for bioservices MultiFASTA read_fasta funtion
    # that recognises only particular headers such as Swissprot(sp) but not Trembl (tr) part of Uniprot...
    # by overriding the read_fasta function -> see bellow (at the end)
    aln = MultiFASTA_extra()
    mapping = {}

    try:
        aln.read_fasta(alnfile)
        for it in range(len(aln.df.Accession)):
            id = aln.df.Accession[it]
            seq = aln.df.Sequence[it]

            mapid = []
            count = 0
            for aa in seq:
                if aa != '-':
                    count += 1
                mapid.append(count)

            mapping[id] = {'seq': seq, 'mapid': mapid}

    except OSError as e:
        print("File error:", sys.exc_info()[0])
        raise

    except:
        print("Unrecognised header type by bioservices MultiFasta... try using something like Uniprot headers 'sp|UkbID|Blabla' ...", sys.exc_info()[0])
        raise

    return mapping




def get_paths_1prot(inputfolder: Path, output: Path, keys: list, protname: str = None) -> dict:
    paths = {};
    for key in keys:
        try:
            if protname is None:
                if key not in ['fasta', 'fsa']:
                    files = list(inputfolder.rglob('*.' + key + '.*'))
                else:
                    files = list(inputfolder.rglob('*.' + key + '*'))
            else:
                if key not in ['fasta', 'fsa']:
                    files = list(inputfolder.rglob(protname + '.' + key + '.*'))
                else:
                    files = list(inputfolder.rglob(protname + '.' + key + '*'))

            if len(files) > 1:
                print("Multiple options: ", list)
                raise
            elif len(files) == 0:
                if (key == 'fasta'):
                    print("In the provided input folder there is no file with either the provided protname : '", protname, \
                      "' or predictor suffix: '", key, "' . Searching for *.fsa...", sep='')
                else:
                    print("In the provided input folder there is no file with either the provided protname : '", protname, \
                      "' or predictor suffix: '", key, "'.", sep='')
            else:
                if protname is None:
                      protname = files[0].name.split('.'+key)[0]
                      print("Within the provided folder, protname : '", protname, \
                      "' was found. Updating protname.", sep='')

                if protname not in paths:
                      paths[protname] = {}
                paths[protname][key] = files[0]

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    return paths



def get_paths_Nprot(inputfolder: Path, output: Path, keys: list) -> dict:
    paths = {};
    for key in keys:
        try:
            if key not in ['fasta', 'fsa']:
                files = list(inputfolder.rglob('*.' + key + '.*'))
            else:
                files = list(inputfolder.rglob('*.' + key + '*'))

            if len(files) == 0:
                if (key == 'fasta'):
                    print("In the provided input folder there is no file with suffix: '", key, "' . Searching for *.fsa...", sep='')
                if (key == 'fsa'):
                    print("In the provided input folder there is no file with suffix: '", key, "' . Searching for *.fasta...", sep='')
                else:
                    print("In the provided input folder there is no file with predictor suffix: '", key, "'.", sep='')

            else:
                for f in files:
                    protname = f.name.split('.'+key)[0]
                    print("Within the provided folder, protname : '", protname, \
                      "' was added.", sep='')

                    if protname not in paths:
                        paths[protname] = {}
                    paths[protname][key] = f

        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    return paths





###############################################################################

#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EMBL-EBI
#
#  File author(s):
#      Sven-Maurice Althoff, Christian Knauth
#
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################


# Temporary fix for bioservices MultiFASTA read_fasta funtion
# that recognises only particular headers such as Swissprot(sp) but not Trembl (tr) part of Uniprot...
# by overriding the read_fasta function

class MultiFASTA_extra(MultiFASTA):

    def read_fasta(self, filename):
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

