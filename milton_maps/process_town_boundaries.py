import geopandas as gpd
from shapely.geometry import MultiPolygon

def process_town_boundaries():

    towns = gpd.read_file("data/raw/townssurvey_shp/TOWNSSURVEY_POLY.shp")
    print(f"There are {towns.TOWN_ID.nunique()} unique towns in the dataset, but the dataframe has shape {towns.shape}, so there are multiple rows per town")

    # The raw dataset contains one row for each disconnected region of a town. For our purposes, we want to merge these into a single multipolygon per town
    town_boundaries_series = towns.groupby("TOWN_ID")['geometry'].agg(lambda x: MultiPolygon(list(x)))
    town_attributes = towns.set_index("TOWN_ID").loc[:, towns.groupby("TOWN_ID").nunique().max()==1].drop_duplicates()

    #There are 351 towns in Massachusetts.  Verify this
    assert town_attributes.shape[0]==351

    #Join multipolygon boundaries to attribute dataframe
    town_boundaries = gpd.GeoDataFrame(town_boundaries_series).merge(town_attributes, left_index=True, right_index=True).set_crs(towns.crs)
    town_boundaries['SHAPE_AREA'] = town_boundaries['geometry'].area  #Square Meters
    town_boundaries['ACRES'] = town_boundaries['SHAPE_AREA'] / 4046.86 # Square meters per acre
    town_boundaries['SQUARE_MIL'] = town_boundaries['SHAPE_AREA'] / 2.59e+6 # Square meters per square mile

    # Sanity checks

    #The Multipolygon's areas should very closely match the sum of shapefile areas over each TOWN_ID
    direct_sum_old_areas = towns.groupby("TOWN_ID")['SHAPE_AREA'].sum()
    assert (town_boundaries['SHAPE_AREA']- direct_sum_old_areas ).divide(direct_sum_old_areas).max() < 1e-9

    #We should have one row per town and 19 columns
    assert town_boundaries.shape == (351,19)

    town_boundaries.to_file("data/processed/town_boundaries.shp.zip", driver='ESRI Shapefile')


if __name__ == "__main__":
    process_town_boundaries()