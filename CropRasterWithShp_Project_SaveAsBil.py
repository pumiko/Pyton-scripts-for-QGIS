# Script for cropping raster data with polygon vectors
# Performs cropping and projection
# Can be used to change raster file type (e.g. from GeoTif to ERSI BIL)

import glob
import os

folder = 'path/to/raster/'
srcfile = folder + 'Land_Use_raster.tif'
prefix = "Land_Use_"
sufix = "_Land_Use_2016_V1.bil"
shpfiles_list = glob.glob('path/to/shapefiles/*.shp')
srs_transform = "-s_srs EPSG:6346 -t_srs EPSG:26917 -r near" 
# Source and Target EPSG code
# near for discrete data like land use
# bilinear for continous data like digital elevation model
na_value = "0"

for shp in shpfiles_list:
	# Get shapefile name (remove folder name and extension)
	# Length hardcoded for purpose of this excersise
    shp_name = shp[64:]
    shp_name = shp[:-4]
    print shp_name
    
    dstfile = folder + "TifFiles/" + prefix + shp_name + ".tif"
    #print dstfile
    
    bil_dstfile = folder + "BilFiles/" + shp_name + sufix
    #print bil_dstfile

    #print "gdalwarp " + srs_transform + " -q -cutline " + shp + " -crop_to_cutline -tr 5.0 5.0 -of GTiff -overwrite " + srcfile + " " +  dstfile
    os.system("gdalwarp " + srs_transform + " -q -cutline " + shp + " -crop_to_cutline -tr 5.0 5.0 -of GTiff -overwrite " + srcfile + " " + dstfile)
    
    #print "gdal_translate -a_nodata " + na_value + " -of EHdr " + dstfile + " " + bil_dstfile
    os.system("gdal_translate -a_nodata " + na_value + " -of EHdr " + dstfile + " " + bil_dstfile)