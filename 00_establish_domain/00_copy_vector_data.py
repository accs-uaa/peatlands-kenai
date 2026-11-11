# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Copy domain vector
# Author: Timm Nawrocki
# Last Updated: 2026-11-11
# Usage: Must be executed in a Python 3.12+ installation.
# Description: 'Copy domain vector' copies a manually created vector domain into the region geopackage.
# ---------------------------------------------------------------------------

# Import packages
import os
import shapely
import geopandas as gpd

#### SET UP DIRECTORIES, FILES, AND FIELDS
####____________________________________________________

# Set root directory
drive = 'C:/'
root_folder = 'ACCS_Work'

# Define folder structure
project_folder = os.path.join(drive, root_folder, 'Projects/VegetationEcology/Pew_Peatland_LowerKenai/data')
akveg_geodatabase = os.path.join(drive, root_folder, 'Projects/VegetationEcology/AKVEG_Map/Data/AKVEG_Map.gdb')
floodplain_geodatabase = os.path.join(
    drive, root_folder,
    'Projects/VegetationEcology/AKVEG_Map/Data/Data_Input/surficial_floodplains/AKVEG_Floodplains_Development.gdb')
region_geopackage = os.path.join(project_folder, 'data_input/region_data/region_data_3338.gpkg')

# Define input files
region_layer = 'lowerkenai_domain_3338'
floodplain_input = 'KenaiSouth_Floodplains'
floodplain_output = 'floodplain_active_boundaries_3338'

#### COPY DOMAIN VECTOR
####____________________________________________________

# Read geometry only (columns=[] skips loading all attribute fields)
region_data = gpd.read_file(akveg_geodatabase, layer=region_layer, columns=[])
floodplain_data = gpd.read_file(floodplain_geodatabase, layer=floodplain_input, columns=[])

# Force geometries to 2D by stripping Z and M coordinate dimensions
region_data['geometry'] = shapely.force_2d(region_data.geometry)
floodplain_data['geometry'] = shapely.force_2d(floodplain_data.geometry)

# Clip floodplain data to the region domain
floodplain_data = gpd.clip(floodplain_data, region_data)

# Calculate geometric length (perimeter) and area
region_data['shape_length'] = region_data.geometry.length
region_data['shape_area'] = region_data.geometry.area
floodplain_data['shape_length'] = floodplain_data.geometry.length
floodplain_data['shape_area'] = floodplain_data.geometry.area

# Create geopackage if it does not already exist
if not os.path.exists(region_geopackage):
    # Write the region data
    region_data.to_file(region_geopackage, layer=region_layer, driver='GPKG', mode='w')
else:
    # Append the region data
    region_data.to_file(region_geopackage, layer=region_layer, driver='GPKG', mode='a')

# Append the floodplain data
floodplain_data.to_file(region_geopackage, layer=floodplain_output, driver='GPKG', mode='a')
