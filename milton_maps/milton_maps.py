import pandas as pd
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
from typing import Tuple
import warnings

def plot_map(gdf: gpd.GeoDataFrame,
             column: str,
             categorical: bool=True,
             axis_scale: float=1,
             legend_shift: float=1,
             figsize: Tuple[int, int]=(20, 20),
             markersize: float=0.01,
             legend: bool=True,
             title: str=None,
             cmap: str='gist_earth') -> matplotlib.axes._subplots.AxesSubplot:
    """Generic function to plot maps from GeoDataFrame.

    Args:
        gdf (geopandas.GeoDataFrame): the GeoDataFrame we want to plot map from.
        column (str): column name that we want to use in the plot.
        categorical (bool): ``True`` if the column should be treated as a categorical variable,
            ``False`` if not. Defaults to ``True``.
        axis_scale (float): the scale to enlarge or shrink the axis. Defaults to ``1`` (no size
            adjustments).
        legend_shift (float): how much to shift the legend box to the right. Defaults to ``1``.
            Larger number will shift the legend box further to the right. This parameter
            is used to prevent overlap of the legend box and the map.
        figsize (tuple): the size of the figure. Defaults to ``(20, 20)``.
        markersize (float): the size of the marker, only useful for GeoDataFrame that contains
            point geometries. Defaults to ``0.01``.
        title (str): the title of the figure. Defaults to ``None``, in which case no title will be
            set.
        coord (str): whether the coordinates are distance based (``'distance'``) or
            latitude-longitude based (``'latlong'``). Defaults to ``'distance'``. Acceptable values
            include ``'distance'``,``'latlong'``.
        cmap (str): the color map to use in the map plot. Defaults to ``'gist_earth'``. The color
            maps available in matplotlib can be found here:
            https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html

    Returns:
        matplotlib.axes._subplots.AxesSubplot: matplotlib plot.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        units = gdf.crs.to_dict()['units']

    if units != 'm':
        raise ValueError(f'coordinate units can only be meters (m). Instead, the crs was: {gdf.crs.to_dict()}')

    fig, ax = plt.subplots(1, figsize=figsize)
    ax.grid()
    gdf.plot(ax=ax, column=column, categorical=categorical, legend=legend, markersize=markersize, cmap=cmap)

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

