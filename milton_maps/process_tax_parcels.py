"""Usage: milton_maps process_tax_parcels TAX_PARCELS ASSESSOR_DBS OUTPUT

Arguments:
  TAX_PARCELS      comma separated list of paths to SHP files containing tax parcels for towns
  ASSESSOR_DBS     comma separated list of paths to pkl files containing cleaned assessor DB dataframes for towns
  OUTPUT           output path to write processed Assessor DB as a pickled dataframe
"""
import sys
from docopt import docopt
import pandas as pd
import geopandas as gpd
import joblib
import milton_maps as mm

def process_tax_parcels(tax_parcel_paths, assessor_db_paths, output):
    tax_parcels = pd.concat([
        gpd.read_file(t) for t in tax_parcel_paths
    ])
    assessor_db = pd.concat([
        joblib.load(a) for a in assessor_db_paths
    ])
    tax_parcels_extended = tax_parcels.set_index("LOC_ID").join(
        assessor_db[["PROP_ID",
                     "LOC_ID",
                     "TOWN",
                     "YEAR_BUILT",
                     "USE_DESCRIPTION",
                     "RES_AREA",
                     "ZONING",
                     "UNITS",
                     "STYLE",
                     "LOT_SIZE",
                     "TOTAL_VAL",
                     "LAND_VAL",
                     "SITE_ADDR",
                     "IS_RESIDENTIAL"]],
        how="outer"
    )
    residential_tax_parcels = tax_parcels_extended[tax_parcels_extended.IS_RESIDENTIAL.fillna(False)]
    joblib.dump(residential_tax_parcels, output)


def main(argv):
    """Console script for processing assessor DB"""
    arguments = docopt(__doc__, argv)
    tax_parcel_paths = arguments['TAX_PARCELS'].split(",")
    assessor_db_paths = arguments['ASSESSOR_DBS'].split(",")
    if len(tax_parcel_paths) != len(assessor_db_paths):
        raise ValueError("Must provide an equal number of tax parcel and assessor db files")

    process_tax_parcels(tax_parcel_paths, assessor_db_paths, arguments['OUTPUT'])


if __name__ == "__main__":
    argv = sys.argv
    sys.exit(main(argv))  # pragma: no cover

