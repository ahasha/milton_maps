import contextily as ctx
import geopandas as gpd
import matplotlib
import matplotlib.pyplot  as plt
import pandas as pd

from typing import Tuple
import warnings

# Use codes as defined by the [codebook](https://www.mass.gov/files/documents/2016/08/wr/classificationcodebook.pdf)

USE_CODES = {
    '101': "Single Family",
    '102': "Condominium",
    '103': "Mobile Home",
    '104': "Two-Family",
    '105': "Three-Family",
    '106': "Accessory Land with Improvement - garage,etc.",
    '109': "Multiple Houses on one parcel (for example, a single and a two-family on one parcel)",
    '132': "Undevelopable Land",
    '930': "Municipal, Vacant, Selectmen or City Council",
    '130': "Vacant Land in a Residential Zone or Accessory to Residential Parcel, Developable Land",
    '343': "Office Building", #There is no code 343 in the cited reference, but prefix 34 indicates office buildings.
    '131': "Vacant Land in a Residential Zone or Accessory to Residential Parcel, Potentially Developable Land",
    '945': "Educational Private, Affilliated Housing",
    '942': "Educational Private, College or University",
    '920': "Department of Conservation and Recreation, Division of Urban Parks and Recreation",
    '340': "General Office Buildings",
    '931': "Municipal, Improved, Selectmen or City Council",
    '960': "Church, Mosque, Synagogue, Temple, etc",
    '325': "Small Retail and Services stores (under 10,000 sq. ft.)",
    '337': "Parking Lots - a commercial open parking lot for motor vehicles",
    '932': "Municipal, Vacant, Conservation",
    '013': "Multiple-Use, primarily Residential",
    '031': "Multiple-Use, primarily Commercial",
    '950': "Charitable, Vacant, Conservation Organizations"
}

# Currently only need mappings for Milton and Quincy. Expand to add more municipalities.
TOWN_IDS = {
    189: "Milton",
    243: "Quincy",
}

RESIDENTIAL_USE_CODES = ['101', '102', '103', '104', '105', '109', '013']

PUBLIC_ACCESS_CODES = {
    "Y": "Yes (open to public)",
    "N": "No (not open to public)",
    "L": "Limited (membership only)",
    "X": "Unknown",
}

LEVEL_OF_PROTECTION_CODES = {
    "P": "In Perpetuity",
    "T": "Temporary",
    "L": "Limited",
    "N": "None",
}

PRIMARY_PURPOSE_CODES = {
    "R": "Recreation (activities are facility based)",
    "C": "Conservation (activities are non-facility based)",
    "B": "Recreation and Conservation",
    "H": "Historical/Cultural",
    "A": "Agricultural",
    "W": "Water Supply Protection",
    "S": "Scenic (official designation only)",
    "F": "Flood Control",
    "U": "Site is underwater",
    "O": "Other (explain)",
    "X": "Unknown"
}

def transform_use_codes(use_codes: pd.Series) -> pd.Series:
    """
    Standardizes use codes by extracting first three digits and looking up description

    USE_CODE – state three-digit use code with optional extension digit to accommodate the four-digit codes commonly used
    by assessors. If the codes contain a four-digit use code, because the meaning of the fourth digit varies from community-to-community,
    the standard requires a lookup table. See the end of this Section for more details on this look-up table.

    """
    def use_codes_map(use_code):
        try:
            use_description = USE_CODES[use_code]
        except KeyError:
            use_description = "Other"
        return use_description

    use_code_descriptions = use_codes.str[:3].map(use_codes_map)
    return use_code_descriptions

def plot_map(gdf: gpd.GeoDataFrame,
             column: str,
             categorical: bool=True,
             axis_scale: float=1,
             legend_shift: float=1,
             figsize: Tuple[int, int]=(20, 20),
             markersize: float=0.01,
             legend: bool=True,
             title: str=None,
             cmap: str='gist_earth',
             fig=None,
             ax=None,
             **style_kwds):
    """Generic function to plot maps from GeoDataFrame.

    Args:
        gdf (geopandas.GeoDataFrame): the GeoDataFrame we want to plot map from.
        column (str): column name that we want to use in the plot.
        categorical (bool): ``True`` if the column should be treated as a categorical variable,
            `               `False`` if not. Defaults to ``True``.
        axis_scale (float): the scale to enlarge or shrink the axis. Defaults to ``1`` (no size
                            adjustments).
        legend_shift (float): how much to shift the legend box to the right. Defaults to ``1``.
                              Larger number will shift the legend box further to the right. This parameter
                              is used to prevent overlap of the legend box and the map.
        figsize (tuple): the size of the figure. Defaults to ``(20, 20)``.
        markersize (float): the size of the marker, only useful for GeoDataFrame that contains
                            point geometries. Defaults to ``0.01``.
        title (str): the title of the figure. Defaults to ``None``, in which case no title will be set.
        cmap (str): the color map to use in the map plot. Defaults to ``'gist_earth'``. The color
                    maps available in matplotlib can be found here:
                    https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
        ax: (matplotlib.axes._subplots.AxesSubplot) matplotlib axis object to add plot to

    Returns:
        matplotlib.axes._subplots.AxesSubplot: matplotlib plot.

    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        units = gdf.crs.to_dict()['units']

    if units != 'm':
        raise ValueError(f'coordinate units can only be meters (m). Instead, the crs was: {gdf.crs.to_dict()}')

    if not ax:
        fig, ax = plt.subplots(1, figsize=figsize)
    ax.grid()
    gdf.plot(ax=ax, column=column, categorical=categorical, legend=legend, markersize=markersize, cmap=cmap, **style_kwds)

    # Shrink current axis by `axis_scale`
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * axis_scale, box.height * axis_scale])

    if legend:
        leg = ax.get_legend()
        if leg is not None:
            leg.set_bbox_to_anchor((legend_shift, 1))

    if units == 'm':
        ax.set(xlabel='distance_x (meters)', ylabel='distance_y (meters)')
    # elif coord == 'latlong':
    #     ax.set(xlabel='longitude (deg)', ylabel='latitude (deg)')

    if isinstance(title, str):
        ax.set_title(title)

    return ax


def make_choropleth_style_function(df: pd.DataFrame,
                                   attr: str, colormap: str,
                                   navalue="None"):
    cmap = matplotlib.cm.get_cmap(colormap)
    attr_values = list(df[attr].fillna(navalue).unique())
    colormap_dict = {attr_values[i]: matplotlib.colors.rgb2hex(cmap(i)) for i in range(len(attr_values))}

    def stylefunc(x):
        val = x['properties'][attr]
        if val is None:
            val = navalue
        return {
            'fillColor': colormap_dict[val],
            'color': colormap_dict[val],
        }

    return stylefunc, colormap_dict


def html_legend(cmap_dict):
    table_html = """<table>
  <tr>
    <th>Value</th>
    <th>Color</th>
  </tr>
""" + "\n".join(
        f'<tr><td><span style="font-family: monospace">{code}</span></td> <td><span style="color: {color}">████████</span></td></tr>'
        for code, color in cmap_dict.items()
    ) + "</table>"

    return table_html

# def add_basemap(ax, zoom, url=ctx.sources.ST_TONER_LITE):
#     xmin, xmax, ymin, ymax = ax.axis()
#     basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax, zoom=zoom, source=url)
#     ax.imshow(basemap, extent=extent, interpolation='bilinear')
#     # restore original x/y limits
#     ax.axis((xmin, xmax, ymin, ymax))


