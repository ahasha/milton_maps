import logging
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

logger = logging.getLogger("process_crash_data")

INJURY_MAP = {
    "No injury": "No Injury",
    "Non-fatal injury - Possible": "Minor Injury",
    "Non-fatal injury - Non-incapacitating": "Minor Injury",
    "Non-fatal injury - Incapacitating": "Major Injury",
    "Not reported": "Unknown",
    "Fatal injury (K)": "Fatal Injury",
    "Unknown": "Unknown",
    "Not Applicable": "No Injury",
    "Deceased not caused by crash": "No Injury",
    "No Apparent Injury (O)": "No Injury",
    "Suspected Minor Injury (B)": "Minor Injury",
    "Possible Injury (C)": "Minor Injury",
    "Suspected Serious Injury (A)": "Major Injury",
}

# define project_root Path object
ROOT_DIR = Path(__file__).parent.parent


def get_milton_boundaries():
    town_boundaries = gpd.read_file(
        ROOT_DIR / "data/processed/town_boundaries.shp.zip"
    ).set_index("TOWN_ID")
    milton_boundaries = town_boundaries[town_boundaries.TOWN.isin(["MILTON"])]
    return milton_boundaries


def get_crash_data(milton_boundaries=None) -> gpd.GeoDataFrame:

    if not milton_boundaries:
        milton_boundaries = get_milton_boundaries()

    # Read in crash data, which is in a CSV file with CRLF line endings, skipping 2 (??) rows.
    crash_data = pd.read_csv(
        ROOT_DIR / "data/raw/MiltonCrashDetails.csv",
        skiprows=2,
        dtype={
            "Maximum_Injury_Severity_Reported": "category",
            "Crash_Severity": "category",
            "At_Roadway_Intersection": "category",
        },
    )
    crash_data.shape

    # combine text Crash_Date and Crash_Time fields into a single datetime field, assuming EST timezone.
    crash_data["Crash_DateTime"] = pd.to_datetime(
        crash_data["Crash_Date"] + " " + crash_data["Crash_Time"], utc=True
    ).dt.tz_convert("EST")
    crash_data["year"] = crash_data["Crash_DateTime"].dt.year
    crash_data["severity"] = (
        crash_data["Maximum_Injury_Severity_Reported"].fillna("Unknown").map(INJURY_MAP)
    )

    """Data transformation notes:

    - [x] Need to parse Crash Date + Crash Time into a datetime field.
    - [ ] Transform Crash Severity into a categorical variable.
    - [ ] Transform Manner of Colission into a categorical variable.
    """

    logger.info(
        f"Found {crash_data[crash_data['X_Cooordinate'].isnull() | crash_data['Y_Cooordinate'].isnull()].shape[0]} records missing coordinates, and will be dropped"
    )
    crash_data = crash_data.dropna(subset=["X_Cooordinate", "Y_Cooordinate"])
    geometry = crash_data.apply(
        lambda row: Point(row["X_Cooordinate"], row["Y_Cooordinate"]), axis=1
    )
    crash_geodf = gpd.GeoDataFrame(data=crash_data, geometry=geometry, crs="EPSG:26986")
    # apply `milton_boundaries` as a mask to the crash_geodf
    crash_geodf2 = gpd.clip(crash_geodf, milton_boundaries)
    # determine how many records were dropped by the geoclip
    logger.info(
        f"Found {crash_geodf.shape[0] - crash_geodf2.shape[0]} records outside Milton were dropped by the geoclip."
    )
    return crash_geodf2


def get_randolph_ave_shape():
    massdot_roads = gpd.read_file(ROOT_DIR / "data/raw/MassDOT_Roads_SHP.zip")
    randolph_ave = massdot_roads.loc[
        (massdot_roads.RT_NUMBER == "28")
        & (massdot_roads.STREET_NAM.str.lower().str.contains("randolph"))
    ]

    return randolph_ave


def randolph_ave_upstream_vs_intersection(crash_geodf=None, randolph_ave=None):
    if randolph_ave is None:
        randolph_ave = get_randolph_ave_shape()

    if crash_geodf is None:
        crash_geodf = get_crash_data()

    # Filter crash points to those within 20 meters of randolph avenue line
    randolph_ave_buffer = randolph_ave.buffer(20)
    # Crash points inside the randolph_ave_buffer
    randolph_ave_crashes = gpd.clip(crash_geodf, randolph_ave_buffer)

    # Create a polygon buffer of 30 meters around the latitude longitude (42.224225, -71.070639), which is the Chickatawbutt/Randolph intersection.
    # in the same CRS as the crash data.
    chickatawbut_randolph_intersection = (
        gpd.GeoSeries(
            Point(-71.070639, 42.224225), crs="EPSG:4326"  # Latitude/Longitude CRS
        )
        .to_crs("EPSG:26986")  # This CRS measures units in meters
        .buffer(20)
    )

    intersection_crashes = gpd.clip(crash_geodf, chickatawbut_randolph_intersection)
    logger.info(f"Intersection crashes shape: {intersection_crashes.shape}")

    upstream_crashes = randolph_ave_crashes.loc[
        ~randolph_ave_crashes.index.isin(intersection_crashes.index), :
    ]
    logger.info(f"Upstream crashes shape: {upstream_crashes.shape}")

    intersection_crashes["where"] = "intersection"
    upstream_crashes["where"] = "upstream"
    combined_crashes = gpd.GeoDataFrame(
        pd.concat([intersection_crashes, upstream_crashes], ignore_index=True)
    )

    return intersection_crashes, upstream_crashes, combined_crashes
