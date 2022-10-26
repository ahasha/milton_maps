"""Usage: milton_maps process_assessor_db INPUT LAYER OUTPUT

Arguments:
  INPUT       path to GDB file containing assessor DB in layer LAYER
  LAYER       layer within GDB file containing asessor DB
  OUTPUT      output path to write processed Assessor DB as a pickled dataframe
"""
import sys
from docopt import docopt
import geopandas as gpd
import joblib
import milton_maps as mm
from fiona.errors import DriverError

def use_codes_map(use_code):
    try:
        use_description = mm.USE_CODES[use_code]
    except KeyError:
        use_description = "Other"

    return use_description

def process_assessor_db(input_path, layer, output_path):
    try:
        assessor_df = gpd.read_file(input_path, layer=layer)
    except ValueError:
        raise ValueError(f"{input_path} does not contain the layer {layer}")
    except DriverError:
        raise ValueError(f"{input_path} does not exist")

    #Append convenience fields
    assessor_df['USE_DESCRIPTION'] = assessor_df['USE_CODE'].map(use_codes_map)
    assessor_df['IS_RESIDENTIAL'] = assessor_df['USE_CODE'].isin(mm.RESIDENTIAL_USE_CODES)

    joblib.dump(assessor_df, output_path)



def main(argv):
    """Console script for processing assessor DB"""
    arguments = docopt(__doc__, argv)
    if arguments['INPUT'][-3:].lower() != "gdb":
        raise ValueError(f"Input file must be a GDB file, got {arguments['INPUT']}")
    output_file = arguments['OUTPUT']
    if arguments['OUTPUT'][-3:].lower() != "pkl":
        output_file += ".pkl"
    process_assessor_db(arguments['INPUT'], arguments['LAYER'], output_file)


if __name__ == "__main__":
    argv = sys.argv
    sys.exit(main(argv))  # pragma: no cover

