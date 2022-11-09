# Jaemin Eun
# Melt-Pond Classification Functions

# In this script, we provide a few important functions used for analyzing melt pond fractions
# from a (seperate) sea-ice classification algorithm using Sentinel-2 imagery.
# The main functions are as follows:
#   1. Assigning projection information from classified HDF files.
#   2. Mosaicing .tif and .h5 layers.
#   3. Calculating Melt Pond Fraction and Sea-Ice concentration.

from osgeo import gdal
import os

import rasterio
from rasterio import mask
from pylab import *
import numpy as np
import sys
import pandas as pd
import h5py
from PIL import Image
import csv

# 1. Assigning projection information for classified HDF files

# The classified HDF files lack georeferencing in their native format. This script uses GDAL
# to georeference the files to the tiff format. This will allow for easier comparisons with
# the actual imagery.

def GDAL_georef(directory, HDF_File, extent, output):
   os.chdir(directory)
   rasterFiles = os.listdir(os.getcwd())

   # We will convert the HDF to a georefferenced tif
   fileExtension = ".tif"

   ### Open the HDF File ###
   hdflayer = gdal.Open(rasterFiles[0], gdal.GA_ReadOnly)
   rlayer = gdal.Open(HDF_File, gdal.GA_ReadOnly)

   # naming output objects
   outputRaster = directory + output + fileExtension

   # Georeferencing with EPSG:32620 (WGS 84 UTM zone 20N)
   EPSG = "-a_srs EPSG:32620"

   translateOptionText = EPSG + " -a_ullr " + extent
   translateoptions = gdal.TranslateOptions(gdal.ParseCommandLine(translateOptionText))
   gdal.Translate(outputRaster, rlayer, options = translateoptions)
   hdflayer = None
   rlayer = None
   return "Classification georefferenced with EPSG 32620"

# These are what we need to pass into the function
directory = 'INSERT FULL DIRECTORY PATH HERE'
HDF_File = 'T20XNS_20220804T192921_classification.h5' #Example HDF output

# Extent is defined by GDAL bounding coordinates i.e. ullon ullat lrlon lrlat
extent = '499980 9200040 609780 9090240' #Provided as an example
output = 'GeorefferencedClassification'

#How to call the function
GDAL_options = GDAL_georef(directory, HDF_File, extent, output)
print(GDAL_options)

# 2. Mosaic function for different classification/imagery types.
#    - Can convert formats to standard tif for easy viewing in a GIS.

def Mosaic(base_direc, output_tif):
   res = [] #Empty list to store files
   # Iterate directory (based on base_direc)
   for file in os.listdir(base_direc):
      #Check only .jp2 files (Could also change to .h5, .nc, or even combine .tif formats)
      if file.endswith('.jp2'):
         res.append(base_direc + file)

   output_src = base_direc + output_tif
   g = gdal.Warp(output_src, res, format = "GTiff", options = ["COMPRESS=LZW", "TILED=YES"])
   g = None #Close file and flush to disk

   return "Bands Merged"

base_direc = 'INSERT FULL PATH DIRECTORY HERE'
output_tif = 'MethodTest.tif' #Provided as an example

# How to call the function
print(Mosaic(base_direc, output_tif))

# 3. Calculating Melt Pond Fraction (MPF) and Sea-Ice Concentration (SIC)
#    - Data returned from the Mosaic function can be passed on to export to csv

def MPF(output_loc):
   data = pd.read_csv(output_loc, delimiter='\t',names=['Tile','IMG_Pixel','Border','Ice','OW','MP','Other'])

   # Calculate MPF and SIC:
   data['MPF'] = data.MP/(data.MP + data.Ice)
   data['SIC'] = (data.Ice + data.MP)/(data.Ice + data.MP + data.OW)
   data['Surface'] = data.IMG_Pixel - data.Border

   # We don't want to calculate melt pond fraction for tiles with a sea-ice concentration less than 15%.
   # For those values, we convert to nan.

   for b in data[data.SIC<.15].index.values:
      data.at[b, 'MPF'] = np.nan

   # Day of Year (For Datetime objects)
   # We parse out the datetime objects based on the file naming conventions
   # The "tile" dataframe includes the tile and the "date" the image was obtained.
   # By parsing out the position of the date values, we can extract datetime objects.
   data['DOY']=[datetime.datetime.strptime(a,'%Y%m%d').timetuple().tm_yday for a in [a[7:15] for a in data.Tile]]

   return data

# Can export MPF objects to csv for instance:
classification_loc = 'ENTER FULL TEXT FILE PATH' # i.e. '~/directory/output.txt'
MPF(classification_loc).to_csv('ENTER FILE NAME YOU WISH TO SAVE CSV WITH FILE EXTENSION')
