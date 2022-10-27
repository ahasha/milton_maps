"""Usage: milton_maps process_tax_parcels INPUT OUTPUT

Arguments:
  INPUT       path to SHP file containing assessor DB in layer LAYER
  OUTPUT      output path to write processed Assessor DB as a pickled dataframe
"""
import sys
from docopt import docopt
import geopandas as gpd
import joblib
import milton_maps as mm

def process_tax_parcels(input_path, output_path):
    pass



def main(argv):
    """Console script for processing assessor DB"""
    arguments = docopt(__doc__, argv)
    if arguments['INPUT'][-3:].lower() != "shp":
        raise ValueError(f"Input file must be a SHP file, got {arguments['INPUT']}")
    output_file = arguments['OUTPUT']
    if arguments['OUTPUT'][-3:].lower() != "pkl":
        output_file += ".pkl"
    process_tax_parcels(arguments['INPUT'], output_file)


if __name__ == "__main__":
    argv = sys.argv
    sys.exit(main(argv))  # pragma: no cover

