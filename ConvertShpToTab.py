# Script for converting ESRI shapefiles into MapInfo TAB file
# With capability of updating attribute table

from qgis.core import *
from PyQt4.QtCore import *
import os
import glob
import processing

# parameters
inPath = "in/Path"
outPath = "out/Path"
epsg = 26917 # NAD83/UTM17N - can be any EPSG code - to determine output file projection

shpList = next(os.walk(inPath))[2]
exp_crs = QgsCoordinateReferenceSystem(epsg, QgsCoordinateReferenceSystem.EpsgCrsId) 

# List shp files
matchingShpList = [s for s in shpList if (".shp" in s)]

for file in matchingShpList:
	# print inPath + file
	
	# Open shapefile
	lyrName = file.rsplit( ".", 1 )[ 0]
	print lyrName
	vLayer = QgsVectorLayer(inPath + file, lyrName, "ogr")
	vLayerData = vLayer.dataProvider()
	if not vLayer.isValid():
	    print "Layer failed to load!"
	
	# Update attribute table of shp shapefile
	# vLayer.startEditing()
	# vLayerData.deleteAttributes([vLayer.fieldNameIndex('Polygon_ID')])
	# vLayerData.addAttributes([QgsField('FID', QVariant.Int)])
	# vLayer.updateFields()
	# for f in processing.features(vLayer):
	# 	vLayer.changeAttributeValue(f.id(), vLayer.fieldNameIndex('FID'), 0)
	# 	vLayer.commitChanges()
	
	# Save as TAB file in outPath folder
	tabName = outPath + vLayer.name() + ".tab"
	#print tabName
	QgsVectorFileWriter.writeAsVectorFormat(vLayer, tabName, "utf-8", exp_crs, 'MapInfo File')
	