# QGIS user script for projecting and merging multiple vector layers
# New column wih name of original file is added to output file
# Similar approach can be used for merging any kind of vector files 
# Sufix is sufix of new file name of output file without extension
# Files folder in this execrice has fixed structure with two folders: Original (already filled with shpfiles to be merged) and wgs84"
# Some parameters are hardcoded for purpose of this exercise


##Sufix=string
##Files_folder=folder

from qgis.core import *
from PyQt4.QtCore import *
import os
import glob
import processing

def convertUTMShpToWGSShp(filesPath):
    # IF folder exist remove all files ELSE IF folder doesn't exist create folder
    inPath = filesPath + "Original/"
    outPath = filesPath + "wgs84/"

    if os.path.isdir(outPath):
        os.chdir(outPath)
        files = glob.glob('*')
        for file in files:
            os.unlink(file)
    else:
        os.makedirs(outPath)

    # List tab files
    shpList = next(os.walk(inPath))[2]
    print shpList
	
    matchingShpList = [s for s in shpList if (".shp" in s)]
    exp_crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
    for file in matchingShpList:
        # Open Tab files
        lyrName = file.rsplit( ".", 1 )[ 0 ]
        print lyrName
        vLayer = QgsVectorLayer(inPath + file, lyrName, "ogr")
        print vLayer

        # Save as SHP file in outPath folder
        shpName = outPath + vLayer.name() + ".shp"
        QgsVectorFileWriter.writeAsVectorFormat(vLayer, shpName, "utf-8", exp_crs,
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


def mergeShapefiles(sufix, filesPath):
    # If folder exist remove all shpfiles ELSE IF folder doesn't exist create folder
    if os.path.isdir(filesPath):
       os.chdir(filesPath)
       files = glob.glob(sufix+".shp")
       for file in files:
           os.unlink(file)
    else:
        os.makedirs(outPath)

    # List files to merge
    shpPath = filesPath + "wgs84/"
    shpList = next(os.walk(shpPath))[2]
    print shpPath
    matchingShpList = [s.strip(".shp") for s in shpList if ".shp" in s]
    print matchingShpList
    # Merge files and save merged shp in new directory
    processing.runalg("qgis:mergevectorlayers", matchingShpList, filesPath + sufix + "_merged_wgs84.shp")
    print filesPath + sufix + "_merged_wgs84.shp"

    for i in QgsMapLayerRegistry.instance().mapLayers().values():
        QgsMapLayerRegistry.instance().removeMapLayer(i.id())

# RUN
# Read parameters (user input)
sufix = str(Sufix)
filesPath = str(Files_folder)+"/"

# Run algorithm
convertUTMShpToWGSShp(filesPath)
mergeShapefiles(sufix, filesPath)