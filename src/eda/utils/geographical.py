"""Code for generating geographical plots

Author: Leodegario Lorenzo II
Date: 29 August 2021
"""

import folium
import numpy as np
from folium import plugins


def geographical_plot(
        data, latitude_column, longitude_column, numerical_column=None,
        name=None, start_loc=(40.7128, -74.0060)):
    """Return folium heatmap of the given geographic data

    A numerical column may also be given so that the value of that
    column will be used as weights in the heat map.

    Parameters
    ----------
    data : pandas DataFrame
        Data frame with geographical data

    latitude_column : str
        Column containing the latitude data

    longitude_column : str
        Column containing the longitude data

    numerical_column : str, default=None
        Column containing the numerical data to be used as weights if
        specified

    name : str, default=None
        Name of the folium map to be used 

    start_loc : tuple, default=(40.7128, -74.0060)
        Default starting location of the visualization. This is set to
        New York City by default.

    Returns
    -------
    m : folium Map
        Folium heatmap containing the geographical data in the data
        frame
    """
    # Make empty map
    m = folium.Map(location=start_loc, zoom_start=10.5,
                   tiles=None, control_scale=True)

    # Add tile layer
    (folium.TileLayer(tiles='cartodbpositron', name=name)
        .add_to(m))

    # Get listing coordinates
    if numerical_column is None:
        listing_coordinates = data.loc[
            :, [latitude_column, longitude_column]
        ].to_numpy()
    else:
        listing_coordinates = data.loc[
            :, [latitude_column, longitude_column, numerical_column]
        ].to_numpy()

    # Set heatmap
    (plugins.HeatMap(np.array(listing_coordinates),
                     min_opacity=0)).add_to(m)

    return m
