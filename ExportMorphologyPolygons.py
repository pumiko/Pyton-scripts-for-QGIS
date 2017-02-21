# QGIS user script for exporting vector features as single shapefiles based on morphology type
# Similar approach can be used for splitting ans saving as single layers any other shapefiles 
# Only reqiurement is some kind of class filed in attribte table
# Some parameters are hardcoded for purpose of this exercise
# Input_layer should be feature layer for user convenience

##Input_layer=string morphology_
##Output_directory=folder
##UTM_zone=number 26900

from qgis.core import *
from PyQt4.QtCore import *
import os
import glob
import processing


def exportMorphologyFiles(inLayer, outDir, utmZone):
    # Read vars form user input
    outDir = outDir
    layer = inLayer
    utmZone = int(utmZone)

    # IF folder exist remove all files ELSE IF folder doesn't exist create folder
    if os.path.isdir(outDir):
        os.chdir(outDir)
        files = glob.glob('*')
        for file in files:
            os.unlink(file)
    else:
        os.makedirs(outDir)

    # Set desitantion params
    crsDest = QgsCoordinateReferenceSystem(utmZone, QgsCoordinateReferenceSystem.EpsgCrsId)
    print crsDest.isValid()
    
    layerList = QgsMapLayerRegistry.instance().mapLayersByName(layer)

    if layerList:
        layer = layerList[0]
        feature = layer.getFeatures()

        # List all morphology names from given layer
        morphoNamesListRaw = []
        for ft in feature:
            attrs = ft['morpho']
            morphoNamesListRaw.append(attrs)
            morphoNamesListRaw
        # print morphoNamesListRaw

        morphoNamesList = set()
        for morpho in morphoNamesListRaw:
            morphoNamesList.add(morpho)
        # print morphoNamesList

        for morpho in morphoNamesList:
            # Select fatures for given morphology
            # 1. Create an expression
            # expr = QgsExpression( "\"Name\"=\'Limpopo\'" )
            expr = QgsExpression("\"morpho\"=" + "\'" + morpho + "\'")
            print "\"morpho\"=" + "\'" + morpho + "\'"
            # 2. Get features from expression
            it = layer.getFeatures(QgsFeatureRequest(expr))
            # Build a list of feature Ids from the result obtained in 2.:
            ids = [i.id() for i in it]
            # Select features with the ids obtained in 3.:
            layer.setSelectedFeatures(ids)

            # Save vector file
            QgsVectorFileWriter.writeAsVectorFormat(layer, outDir + "/" + morpho + ".shp", "utf-8", crsDest,
                                                    "ESRI Shapefile", True)

            layer.removeSelection()


# RUN
# Read parameters (user input)
inLayer = str(Input_layer)
outDir = str(Output_directory)
utmZone = str(UTM_zone)

# Run algorithm
exportMorphologyFiles(inLayer, outDir, utmZone)	