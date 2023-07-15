"""Usage: milton_maps process_openspace INPUT OUTPUT

Arguments:
  INPUT       path to SHP file containing assessor DB in layer LAYER
  OUTPUT      output path to write processed Assessor DB as a pickled dataframe
"""
import sys

import click
import geopandas as gpd

import milton_maps as mm


def process_openspace(input_path, output_path):
    openspace = gpd.read_file(input_path)

    # Manager is only populated when it differs from owner.  Backfill to make field human-readable
    openspace["MANAGER"] = openspace["FEE_OWNER"].fillna(openspace["MANAGER"])

    # Replace codes with human-readable fields
    openspace["PUB_ACCESS"] = openspace["PUB_ACCESS"].map(mm.PUBLIC_ACCESS_CODES)
    openspace["PRIM_PURP"] = openspace["PRIM_PURP"].map(mm.PRIMARY_PURPOSE_CODES)
    openspace["LEV_PROT"] = openspace["LEV_PROT"].map(mm.LEVEL_OF_PROTECTION_CODES)

    openspace.to_file(output_path, driver="ESRI Shapefile")


@click.command()
@click.argument("input_path")
@click.argument("output_path")
def main(input_path, output_path):
    """Console script for processing assessor DB"""
    if input_path[-3:].lower() != "shp":
        raise ValueError(f"Input file must be a SHP file, got {input_path}")
    output_file = output_path
    if output_path[-7:].lower() != "shp.zip":
        output_file += ".shp.zip"
    process_openspace(input_path, output_file)


if __name__ == "__main__":
    argv = sys.argv
    sys.exit(main(argv))  # pragma: no cover
