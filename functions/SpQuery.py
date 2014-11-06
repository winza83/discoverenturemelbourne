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

num = 0
for i in range(layer.GetFeatureCount()):
	for j in range(layer.GetFeature(i).GetFieldCount()):
		name = layer.GetLayerDefn().GetFieldDefn(j).GetName()
		value = layer.GetFeature(i).GetField(name)
		print "num " + str(num) + "|" + name + ": " + str(value)
	num+=1



import os, gdal, json, ogr
driver = gdal.GetDriverByName('ESRI Shapefile')
shp = ogr.Open('/var/www/event/data/SDM136453/ll_gda94/sde_shape/whole/VIC/PTV/layer/ptv_bus_route_metro.shp', 0)
layer = shp.GetLayer()
layer.GetFeatureCount()

layer.SetAttributeFilter("RTPATHDESC like '734%'")
for feature in layer:
	data = json.loads(feature.ExportToJson())
	json.dump(data, open('test2', 'w'))

map[0].data.loadGeoJson('http://124.190.54.81/event/data/test2')



