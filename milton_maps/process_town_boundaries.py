"""Usage: milton_maps process_town_boundaries INPUT OUTPUT

Arguments:
  INPUT       path to GDB file containing assessor DB
  OUTPUT      output path to write processed Assessor DB as a pickled dataframe
"""
import sys
from docopt import docopt
import geopandas as gpd
import json
import logging
from shapely.geometry import MultiPolygon

def process_town_boundaries(input_path, output_path):
    """"""

    towns = gpd.read_file(input_path)
    logging.info(f"There are {towns.TOWN_ID.nunique()} unique towns in the dataset, but the dataframe has shape {towns.shape}, so there are multiple rows per town")

    # The raw dataset contains one row for each disconnected region of a town. For our purposes, we want to merge these into a single multipolygon per town
    town_boundaries_series = towns.groupby("TOWN_ID")['geometry'].agg(lambda x: MultiPolygon(list(x)))
    town_attributes = towns.set_index("TOWN_ID").loc[:, towns.groupby("TOWN_ID").nunique().max()==1].drop_duplicates()

    # There are 351 towns in Massachusetts.  Validate the data against this fact.
    assert town_attributes.shape[0]==351

    # Join multipolygon boundaries to attribute dataframe
    town_boundaries = gpd.GeoDataFrame(town_boundaries_series).merge(town_attributes, left_index=True, right_index=True).set_crs(towns.crs)
    town_boundaries['SHAPE_AREA'] = town_boundaries['geometry'].area  #Square Meters
    town_boundaries['ACRES'] = town_boundaries['SHAPE_AREA'] / 4046.86 # Square meters per acre
    town_boundaries['SQUARE_MIL'] = town_boundaries['SHAPE_AREA'] / 2.59e+6 # Square meters per square mile

    # Sanity checks
    # 1. Check that "TOWN" has not been dropped (it should be a uniquely associated with TOWN_ID) and save the TOWN_ID=>TOWN mapping
    assert "TOWN" in town_boundaries.columns

    # 2. The Multipolygon's areas should very closely match the sum of shapefile areas over each TOWN_ID
    direct_sum_old_areas = towns.groupby("TOWN_ID")['SHAPE_AREA'].sum()
    assert (town_boundaries['SHAPE_AREA']- direct_sum_old_areas ).divide(direct_sum_old_areas).max() < 1e-9

    # 3. We should have one row per town and 19 columns
    assert town_boundaries.shape == (351,19)

    # Save consolidated shapefile
    town_boundaries.to_file(output_path, driver='ESRI Shapefile')
    # Save town_id => town name mapping for downstream use.  Note json format converts integer keys to strings.
    with open("data/processed/town_ids.json", 'w') as f:
        json.dump(town_boundaries["TOWN"].to_dict(), f)

def main(argv):
    """Console script for processing assessor DB"""
    arguments = docopt(__doc__, argv)
    if arguments['INPUT'][-3:].lower() != "shp":
        raise ValueError(f"Input file must be a SHP file, got {arguments['INPUT']}")
    output_file = arguments['OUTPUT']
    if arguments['OUTPUT'][-3:].lower() != "zip":
        output_file += "zip"
    process_town_boundaries(arguments['INPUT'], output_file)


if __name__ == "__main__":
    argv = sys.argv
    sys.exit(main(argv))  # pragma: no cover

