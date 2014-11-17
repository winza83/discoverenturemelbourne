#! /usr/bin/python
import os, gdal, json, ogr
import cgi
import cgitb
cgitb.enable()
import os
import urllib as url

form = cgi.FieldStorage()
refered = os.environ['REQUEST_URI']

if form.getvalue('mode') == 'train':
	mode = 0
elif form.getvalue('mode') == 'bus':
	mode = 2
elif form.getvalue('mode') == 'tram':
	mode = 1
elif form.getvalue('mode') == 'nightrider':
	mode = 4
elif form.getvalue('mode') == 'vline':
	mode = 3
else:
	mode = 3
linenum = form.getvalue('linenum')

driver = gdal.GetDriverByName('ESRI Shapefile')
shp = ogr.Open('/var/www/event/data/bus/ll_gda94/sde_shape/whole/VIC/PTV/layer/ptv_bus_route_metro.shp', 0)
if mode == 0 or mode == 3:
	shp = ogr.Open('/var/www/event/data/train/ll_gda94/sde_shape/whole/VIC/VMLITE/layer/vmlite_tr_rail.shp', 0)
	query = "NAME like '%" + (linenum.upper() + "%").replace("%","%'").replace("'","") + "'"
elif mode == 1:
	shp = ogr.Open('/var/www/event/data/tram/ll_gda94/sde_shape/whole/VIC/PTV/layer/ptv_tram_route.shp', 0)
	query = "PUBDESCSHT like '" + str(linenum) + "'"
else:
	shp = ogr.Open('/var/www/event/data/bus/ll_gda94/sde_shape/whole/VIC/PTV/layer/ptv_bus_route_metro.shp', 0)
	query = "RTPATHDESC like '" + str(linenum) + "%'"

layer = shp.GetLayer()
layer.GetFeatureCount()
layer.SetAttributeFilter(query)

#map[0].data.loadGeoJson('http://124.190.54.81/event/data/test2')

print "Content-type: text/plain \n"
layer.SetAttributeFilter(query)
lst = []
print """
{
  "type": "FeatureCollection",
  "features": [
"""
cnt = 1
for feature in layer:
	i =  feature.ExportToJson()
	lst.append(str(i))

for i in range(len(lst)):
	if (cnt < len(lst)):
		print lst[i] + ","
	else:
		print lst[i]
	cnt += 1
print "]}"