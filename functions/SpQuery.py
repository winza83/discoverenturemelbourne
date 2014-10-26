import os, gdal, json, ogr

driver = gdal.GetDriverByName('ESRI Shapefile')
shp = ogr.Open('/var/www/event/data/layer/ptv_bus_route_metro.shp')
layer = shp.GetLayer()
layer.SetAttributeFilter("DESCSHORT = '705i'")
j = (layer.GetFeature(0)).ExportToJson()

data = json.loads(j)
json.dump(data, open('test', 'w'))


num = 0
for i in range(layer.GetFeatureCount()):

	for j in range(layer.GetFeature(i).GetFieldCount()):
		name = layer.GetLayerDefn().GetFieldDefn(j).GetName()
		value = layer.GetFeature(i).GetField(name)
		print "num " + str(num) + "|" + name + ": " + str(value)
	num+=1


import os, gdal, json, ogr
shp = ogr.Open('/Users/Winza/Desktop/SDM127241/ll_gda94/sde_shape/whole/VIC/PTV/layer/ptv_bus_route_metro.shp', 0)
layer = shp.GetLayer()
layer.GetFeatureCount()

layer.SetAttributeFilter("RTPATHDESC like '734out'")


num = 0
for i in range(layer.GetFeatureCount()):
	for j in range(layer.GetFeature(i).GetFieldCount()):
		name = layer.GetLayerDefn().GetFieldDefn(j).GetName()
		value = layer.GetFeature(i).GetField(name)
		print "num " + str(num) + "|" + name + ": " + str(value)
	num+=1

