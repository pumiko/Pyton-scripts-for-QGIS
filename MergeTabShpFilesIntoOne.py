# QGIS user script for merging and projecting multiple vector layers
# New column wih name of original file is added to output file
# Similar approach can be used for merging any kind of vector files 
# Name is name of output file without extension
# Input folder with files to merge
# Flag parameter should be used when input folder consist more tiles then we want to focus on
# Only requirement to use Flag is existence of pattern that distinguish files of interest
# Some parameters are hardcoded for purpose of this exercise

##Output_fie_name=string
##Input_folder=folder
##Output_folder=folder
##Flag=string

from qgis.core import *
from PyQt4.QtCore import *
import os
import glob
import processing

def convertTabToShp(inPath, outPath, vFlag):
	# Define export crs - output files must be in WGS84
	exp_crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)

	# IF folder exist remove all files ELSE IF folder doesn't exist create folder
    shpPath = outPath + "SHP/"
    if os.path.isdir(shpPath):
        os.chdir(shpPath)
        files = glob.glob('*')
        for file in files:
            os.unlink(file)
    else:
        os.makedirs(shpPath)

    # List tab files
    tabList = next(os.walk(inPath))[2]
    matchingTabList = [s for s in tabList if (vFlag in s and ((".tab" in s) or (".TAB" in s)))]
    for file in matchingTabList:
        # Open Tab files
        lyrName = file.rsplit( ".", 1 )[ 0 ]
        vLayer = QgsVectorLayer(inPath + file, lyrName, "ogr")
        print vLayer

        # Save as SHP file in outPath folder
        shpName = shpPath + vLayer.name() + ".shp"
        QgsVectorFileWriter.writeAsVectorFormat(vLayer, shpName , "utf-8", exp_crs,
                                                'ESRI Shapefile')

        # Add column OrigFile and fill it with lyrName to newly created shp File
        shpLayer = QgsVectorLayer(shpName, lyrName, "ogr")
        shpLayerData = shpLayer.dataProvider()
        shpLayer.startEditing()
        shpLayerData.addAttributes([QgsField('OrigFile', QVariant.String)])
        shpLayer.updateFields()

        # Update column with original file name
        for f in processing.features(shpLayer):
            shpLayer.changeAttributeValue(f.id(), shpLayer.fieldNameIndex('OrigFile'), lyrName)

        shpLayer.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(shpLayer)


def mergeShapefiles(file_name, outPath):
    # If folder exist remove all shpfiles ELSE IF folder doesn't exist create folder
    if os.path.isdir(outPath):
       os.chdir(outPath)
       files = glob.glob(file_name+".shp")
       for file in files:
           os.unlink(file)
    else:
        os.makedirs(outPath)

    # List files to merge
    shpPath = outPath + "SHP/"
    shpList = next(os.walk(shpPath))[2]
    # print shpPath
    matchingShpList = [s.strip(".shp") for s in shpList if ".shp" in s]
    # print matchingShpList
    
	# Merge files and save merged shp in new directory
    processing.runalg("qgis:mergevectorlayers", matchingShpList, outPath + file_name + ".shp")
    print outPath + file_name + ".shp"

    for i in QgsMapLayerRegistry.instance().mapLayers().values():
        QgsMapLayerRegistry.instance().removeMapLayer(i.id())

		
# RUN
# Read parameters (user input)
file_name = str(Output_file_name)
inPath = str(Input_folder)+"/"
outPath = str(Output_folder)+"/"
vFlag = str(flag)

# Run algorithm
convertTabToShp(inPath, outPath, vFlag)
mergeShapefiles(file_name, outPath)