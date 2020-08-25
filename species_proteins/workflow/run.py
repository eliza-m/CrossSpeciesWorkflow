import click
from bioservices.apps import FASTA
from pathlib import Path
import sys

from species_proteins.glycosylation.Glycosylation_pred import Glycosylation_pred
from species_proteins.glycosylation.Netcglyc_data import Netcglyc_data
from species_proteins.glycosylation.Netoglyc_data import Netoglyc_data
from species_proteins.glycosylation.Netnglyc_data import Netnglyc_data
from species_proteins.glycosylation.Glycomine_data import Glycomine_data
from species_proteins.glycosylation.Nglyde_data import Nglyde_data

from species_proteins.acetylation.Acetylation_pred import Acetylation_pred
from species_proteins.acetylation.Gpspail_data import Gpspail_data
from species_proteins.acetylation.Netacet_data import Netacet_data

# from species_proteins.phosphorylation.Phosphorylation_pred import Phosphorylation_pred
from species_proteins.phosphorylation.Netphos_data import Netphos_data
from species_proteins.phosphorylation.Netphospan_data import Netphospan_data
from species_proteins.phosphorylation.Musitedeep_data import Musitedeep_data



@click.group(chain=True, invoke_without_command=True)
def cli():
    pass


@cli.command()
@click.option('--uniprot', required=True, help='Id of the protein to fetch')
@click.option('--filename', required=False, help='filename to save')
def get_fasta(uniprot: str, filename: str = None):
    """Simple program that greets NAME for a total of COUNT times."""
    click.echo(f"receiving fasta sequence for uniprot id ${uniprot}")
    f: FASTA = FASTA()
    f.get_fasta(uniprot)  # bioservices use ugly mutable getters
    output = uniprot + ".fasta" if filename is None else (filename if ".fasta" in filename else filename + ".fasta")
    click.echo(f"saving protein fasta to ${output}")
    f.save_fasta(output)
    return output



@cli.command()
@click.option('--predictor', required=True, help='Name of the predictor to use')
@click.option('--input', required=True, help='Input fasta file path')
@click.option('--output', required=True, help='Output file')
@click.option('--type', required=False, help='Additional arguments to be passed; predictor specific')
def submit_online(predictor: str, input: Path, output: Path, type: str = None):
    """Submit online jobs for a given predictor"""

    # Predictors that can be run online

    predictors = [
        # glycosylation
        'netcglyc', 'netnglyc', 'netoglyc', 'glycomine', 'nglyde',
        # acetylation
        'netacet', 'gpspail',
        # phosphorylation
        'netphos', 'netphospan'
    ]

    if predictor not in predictors:
        print("Unknown predictor key: ", predictor)
        print("Try one of the following :\n", predictors)
        raise

    # GLYCOSYLATION
    elif predictor == 'netcglyc':
        Netcglyc_data.submit_online(input, output)
    elif predictor == 'netoglyc':
        Netoglyc_data.submit_online(input, output)
    elif predictor == 'netnglyc':
        Netnglyc_data.submit_online(input, output)
    elif predictor == 'nglyde':
        Nglyde_data.submit_online(input, output)
    elif predictor == 'glycomine':
        if type not in "NOC":
            print("Glycomine requires selecting a type: 'N', 'C' or 'O' for N/O/C-linked glycosylation prediction")
            raise
        Glycomine_data.submit_online(input, output, type)

    # ACETYLATION
    elif predictor == 'netacet':
        Netacet_data.submit_online(input, output)
    elif predictor == 'gpspail':
        Gpspail_data.submit_online(input, output)

    # PHOSPHORYLATION
    elif predictor == 'netphos':
        Netphos_data.submit_online(input, output)
    elif predictor == 'netphospan':
        Netphospan_data.submit_online(input, output)



@cli.command()
@click.option('--format', required=True, help='"single" or "multi" protein layout')
@click.option('--module', required=False, help='prediction module; accepted values: \n\
                                all            :  All modules \n\
                                all_nonstruct  :  All except structural module (which is slow) \n\
                                ptsmod         :  All Post Translation modifications ( glyc + acet + phos + sumo) \n\
                                struct         :  Structural module \n\
                                glyc           :  Glycosylation module\n\
                                phos           :  Phosphorylation module\n\
                                acet           :  Acetylation module\n\
                                sumo           :  Sumoylation module\n\
                                loc            :  Cellular localisation module' )
@click.option('--inputfolder', required=True, help='Input folder where all prediction results are stored')
@click.option('--output', required=True, help='Output formatted file')
@click.option('--signif', required=False, help='Print only significant predictions. Default: false')
@click.option('--protname', required=False, help='Only for single protein format, when within the specified input \
                folder there are multiple files with the same extension, a basename of the protein should be provided. \
                Example: protname.predictor.out; Default: null')
def format_output(format: str, module: str, inputfolder: Path, output: Path, signif: bool = False,
                 protname: str = None):
    """
        Format output according to their module
        For the moment it assumes that all prediction files are within the same file.
        Not all available options are yet implemented
    """

    keys = {
        'glyc' : ["netnglyc", "nglyde", "glycomineN", "netoglyc", "isoglyp", "glycomineO", "netcglyc",
            "glycomineC", "fasta", "fsa"],
        'acet': ["netacet", "gpspail", "fasta", "fsa"],
        'phos': ["netphos", "netphospan", "musitedeepY", "musitedeepST", "fasta", "fsa"]
    }

    if format == 'single':

        if module in keys:
            inputfolder=Path(inputfolder);
            paths = get_paths_1prot(inputfolder, output, keys[module], protname);

            if     module == 'glyc': predictions = Glycosylation_pred.parse_all(paths)
            elif   module == 'acet': predictions = Acetylation_pred.parse_all(paths)
            # elif   module == 'phos': predictions = Phosphorylation_pred.parse_all(paths)

            predictions.print_1prot(outputfile=output, addseq=True, signif=signif)


        else:
            print("Not yet implemented...")
    else:
        print("Not yet implemented...")







def get_paths_1prot(inputfolder: Path, output: Path, keys: list, protname: str = None) -> dict:
    paths = {};
    for key in keys:
        try:
            if protname is None:
                files = list(inputfolder.rglob('*.' + key + '*'))
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


if __name__ == '__main__':
    cli()
