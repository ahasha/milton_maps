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
import json
import milton_maps as mm
from fiona.errors import DriverError


def process_assessor_db(input_path, layer, output_path):
    try:
        assessor_df = gpd.read_file(input_path, layer=layer)
    except ValueError:
        raise ValueError(f"{input_path} does not contain the layer {layer}")
    except DriverError:
        raise ValueError(f"{input_path} does not exist")

    # LOC_ID is globally unique, but is sometimes missing.  TOWN_ID + PROP_ID is guaranteed to be unique,
    # so we replace LOC_ID with the combination of those two fields when missting.
    assessor_df.index = assessor_df.LOC_ID.fillna(assessor_df.TOWN_ID.astype(str) + assessor_df.PROP_ID)

    # Clean up multiple spaces in site address field
    assessor_df['SITE_ADDR'] = assessor_df['SITE_ADDR'].str.split().str.join(' ')

    # Append human-readable fields
    assessor_df['USE_DESCRIPTION'] = mm.transform_use_codes(assessor_df.USE_CODE)
    assessor_df['IS_RESIDENTIAL'] = assessor_df['USE_CODE'].str[:3].isin(mm.RESIDENTIAL_USE_CODES)

    with open("data/processed/town_ids.json", 'r') as f:
        town_ids_map = json.load(f)

    assessor_df['TOWN'] = assessor_df['TOWN_ID'].astype(str).map(town_ids_map)
    # Check all IDs were mapped
    assert not assessor_df['TOWN'].isnull().values.any()

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
