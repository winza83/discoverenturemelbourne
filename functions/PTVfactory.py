#! /usr/bin/python
import hmac
from hashlib import sha1
import urllib as url
import json as j

class Trans(object):
	def __init__(self, googleKey, key, devid):
		self.googleKey = googleKey
		self.baseurl = "http://timetableapi.ptv.vic.gov.au"
		self.key = key
		self.devid = devid
		h = hmac.new(self.key,'',sha1)
		return None

	def stopsNearBy(self, lat, lng):
		request = "/v2/nearme/latitude/" + str(lat) + "/longitude/" + str(lng)
		return self.getReq(request)

	def HealthCheck(self):
		request = "/v2/healthcheck"
		return self.getReq(request)

	def search(self, loc):
		try:
			doc = url.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address=' + loc + '%20Victoria%20Australia&key=' + self.googleKey)
			data = j.load(doc)
			lat = data['results'][0]['geometry']['location']['lat']
			lng = data['results'][0]['geometry']['location']['lng']
			return self.stopsNearBy(lat, lng)
		except:
			print "Type in a value!"
			return None


	def POI(self, pois, lat1, lng1, lat2, lng2, griddepth, limit):
		poi = ",".join([str(x) for x in pois])
		request = "/v2/poi/" + poi + "/lat1/" + str(lat1) + "/long1/" + str(lng1) + "/lat2/" + str(lat2) + "/long2/" + str(lng2) + "/griddepth/" + str(griddepth) + "/limit/" + str(limit)
		return self.getReq(request)

	def BND(self, mode, stop, limit):
		request = "/v2/mode/" + str(mode) + "/stop/" + str(stop) + "/departures/by-destination/limit/" + str(limit)
		return self.getReq(request)

	def getReq(self, request, time=None):
		h = self.resetH()
		reqstr = ''
		if time is not None:
			h.update(request + "?for_utc=" + time + "&devid=" + str(self.devid))
			signature = h.hexdigest().upper()
			reqstr = self.baseurl + request + "?for_utc=" + time + "&devid=" + str(self.devid) +"&signature=" + signature
		else:
			h.update(request + "?devid=" + str(self.devid))
			signature = h.hexdigest().upper()
			reqstr = self.baseurl + request + "?devid=" + str(self.devid) +"&signature=" + signature
		return reqstr

	def resetH(self):
		h = None
		h = hmac.new(self.key,'',sha1)
		return h

	def SND(self, mode, line, stop, directionid, limit, time=None):
		request = "/v2/mode/" + str(mode) + "/line/" + str(line) + "/stop/" + str(stop) + "/directionid/" + str(directionid) + "/departures/all/limit/" + str(limit)
		if time is not None:
			newreq = self.getReq(request, time)
		else:
			newreq = self.getReq(request)
		return newreq

	def stoppingPattern(self, mode, run, stop, time):
		request = "/v2/mode/" + str(mode) + "/run/" + str(run) + "/stop/" + str(stop) + "/stopping-pattern"
		newreq = self.getReq(request, time)
		return newreq

	def stopsOnLine(self, mode, line):
		request = "/v2/mode/" + str(mode) + "/line/" + str(line) + "/stops-for-line"
		return self.getReq(request)

	def getData(self, request):
		try:
			doc = url.urlopen(request)
			data = j.load(doc)
			return data
		except Exception:
			print "something is wrong"

	def readableData(self, data):
		return str(j.dumps(data, indent=4))

	def delegator(self, method, param):
		reqstr = ""
		if (method == 'stopsNearBy'):
			a, b = param
			reqstr = self.stopsNearBy(a,b)
		elif (method == 'search'):
			a = param[0]
			reqstr = self.search(a)
		elif (method == 'POI'):
			a, b, c, d, e, f, g = param
			reqstr = self.POI(a, b, c, d, e, f, g)
		elif (method == 'BND'):
			a, b, c = param
			reqstr = self.BND(a, b, c)
		elif (method == 'SND'):
			if len(param) == 6:
				a, b, c, d, e, f = param
				reqstr = self.SND(a, b, c, d, e, f)
			else:
				a, b, c, d, e = param
				reqstr = self.SND(a, b, c, d, e)
		elif (method == 'stoppingPattern'):
			a, b, c, d = param
			reqstr = self.stoppingPattern(a, b, c, d)
		elif (method == 'stopsOnLine'):
			a, b = param
			reqstr = self.stopsOnLine(a, b)
		return reqstr