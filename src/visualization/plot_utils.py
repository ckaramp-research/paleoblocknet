# ---
# File: plot_utils.py 
# Author: Christina Karamperidou
# Institution: University of Hawaii at Manoa, Department of Atmospheric Sciences
# Date Created: June 2022
# Description: This file contains custom utility functions for plotting purposes 
# ---

# Import necessary libraries
import numpy as np 
import xarray as xr
from matplotlib.path import Path
from cartopy.util import add_cyclic_point


# polar map 
def polar_set_latlim(lat_lims, ax,data_crs):
    ax.set_extent([-180, 180, lat_lims[0], lat_lims[1]], crs=data_crs)
    # Compute a circle in axes coordinates, acts as boundary for the map
    theta = np.linspace(0, 2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = Path(verts * radius + center)

    ax.set_boundary(circle, transform=ax.transAxes)

# Generate data with cyclic point
def add_cyclic_point_to_dataarray(da):
    # Load data
    data = da

    cyclic_data, cyclic_longitude = add_cyclic_point(data.values, coord=data['lon'])

    # Create new coords that will be used in creation of new dataset
    # Replicate coords of existing dataset and replace longitude with cyclic longitude
    coords = {dim: data.coords[dim] for dim in data.dims}
    coords["lon"] = cyclic_longitude

    new_da = xr.DataArray(cyclic_data, dims=data.dims, coords=coords)
    return new_da


