from pathlib import Path
import sys
from species_proteins.util.MultiFASTA_extra import MultiFASTA_extra



def map_aln( alnfile : Path ) -> dict:
    """
    Maps alignments positions to individual sequences resids.

    Parameters
    ----------
    alnfile : Path
        Alignment file in FASTA format.

    Returns
    -------
    dict:
        Mapped resids.
    """

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




def get_paths_1prot(inputfolder: Path, keys: list, protname: str = None) -> dict:
    """
    Retrieves paths of the raw prediction output files.

    Parameters
    ----------
    inputfolder: Path
        Folder containing raw prediction data.

    keys: list
        List of keys to search prediction results.

    protname : string
        Optional. If multiple files with the same keys are found, an error will be raised to provide protname as
        an additional keyword to deal with ambiguities.

    Returns
    -------
    dict
        Dictionary with all paths structured based on protnames and predictors detected within the provided folder.

    """
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



def get_paths_Nprot(inputfolder: Path, keys: list) -> dict:
    """
    Retrieves paths of the raw prediction output files.

    Parameters
    ----------
    inputfolder: Path
        Folder containing raw prediction data.

    keys: list
        List of keys to search prediction results.

    Returns
    -------
    dict
        Dictionary with all paths structured based on protnames and predictors detected within the provided folder.
    """

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

