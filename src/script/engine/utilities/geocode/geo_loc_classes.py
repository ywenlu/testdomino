# APIs for geoding
# v 1.1.0
# py 3.x

import urllib
import re
import numpy as np
import simplejson

from urllib.parse import urlencode
from urllib.request import urlopen
from jellyfish import levenshtein_distance as levdist

# Initialize OSM geolocator
from geopy.geocoders import Photon
geolocator = Photon()

def format_str(s):
	s = str(s).upper()
	pattern = re.compile(", | ")
	s = sorted(pattern.split(s))
	return " ".join([ss.upper() for ss in s])

class GeoLoc(object):
	"""docstring for GeoLoc"""
	def __init__(self, query):
		self.query = query
		self.geometry = {'coordinates': [str(np.nan), str(np.nan)], 'type': 'Point'}
		self.properties = {'address': None, 'city': None, 'postalcode': None, 'state': None, 'country': None}
		self.score = 999


	def match_score(self):
		try:
			q = self.query
			r = self.get_resp_address()
			if all((r, q)):
				q, r = format_str(q), format_str(r)
				self.score = levdist(q, r)
		except:
			pass
		

class osm(GeoLoc):

	def __init__(self, query):
		GeoLoc.__init__(self, query)
		self.locator = self.get_location(query)
		self.get_properties()
		self.get_geometry()
		self.match_score()
	
	def get_location(self, query):
		try:
			#print("Ok...")
			return geolocator.geocode(query)
		except:
			#print("%s Not found by OSM API!" % query)
			return None

	def get_geometry(self):
		try:
			self.geometry = self.locator.raw['geometry']
		except:
			pass

	def get_latitude(self):
		try:
			return self.locator.latitude
		except:
			return np.nan

	def get_longitude(self):
		try:
			return self.locator.longitude
		except:
			return np.nan

	def get_address(self, locator):
		if locator is not None:
			prop = locator.raw['properties']
			try:
				street = str(prop['street']).strip()
			except:
				try:
					street = str(prop['name']).strip()
				except:
					street = ""
			try:
				num = str(prop['housenumber']).strip()
				return num + " " + street
			except:
				return street
		return None

	def get_prop(self, locator, property = None):
		if locator is not None:
			prop = locator.raw['properties']
			if property == 'address':
				return self.get_address(locator)
			try:
				return str(prop[property]).strip()
			except:
				return None
		return None

	def get_properties(self):
		try:
			self.properties = {'address': self.get_prop(self.locator, "address"),
					'city': self.get_prop(self.locator, "city"),
					'postalcode': self.get_prop(self.locator, "postcode"),
					'state': self.get_prop(self.locator, "state"),
					'country': self.get_prop(self.locator, "country")}
		except:
			pass

	def get_resp_address(self):
		try:
			loc = self.properties
			return ", ".join([loc['address'], loc['postalcode'], loc['city'], loc['state'], loc['country']])
		except:
			return None


class gg(GeoLoc):

	def __init__(self, query):
		GeoLoc.__init__(self, query)
		self.locator = self.get_location(query)
		self.match_score()
		self.get_properties()
		self.get_geometry()

	def get_location(self, query, from_sensor=False):
		# Return the full search result as a dict

		googleGeocodeUrl = 'https://maps.googleapis.com/maps/api/geocode/json?'
		key = "AIzaSyDR5EjuMSzYCTIjQn_FlmPUFVzIbacloas"

		query = query.encode('utf-8')

		params = {
			'address': query,
			'sensor': "true" if from_sensor else "false",
			'key': key
		}
		try:
			url = googleGeocodeUrl + urlencode(params)
			json_response = urlopen(url)
			response = simplejson.loads(json_response.read())
		except:
			return None

		if response['results']:
			#print("Ok...")
			return response
		else:
			#print("%s not found by Google API!" % query)
			return None

	def get_longitude(self):
		try:
			return self.geometry['coordinates'][0]
		except:
			return np.nan

	def get_latitude(self):
		try:
			return self.geometry['coordinates'][1]
		except:
			return np.nan

	def get_geometry(self):
		if self.score == 999:
			return None
		try:
			results = self.locator['results'][0]
			geo = results['geometry']['location']
			self.geometry = {'coordinates': [geo['lng'], geo['lat']], 'type': 'Point'}
		except:
			pass

	def get_address_components(self):
		try:
			results = self.locator['results'][0]
			address_components = results['address_components']
			return {ac['types'][0]: {'long_name': ac['long_name'], 'short_name': ac['short_name']} for ac in address_components}
		except:
			return None

	def get_properties(self):
		try:
			loc = self.get_address_components()
			self.properties = {'address': loc['street_number']['long_name'] + " " + loc['route']['long_name'],
					'city': loc['locality']['long_name'],
					'postalcode': loc['postal_code']['long_name'],
					'state': loc['administrative_area_level_1']['long_name'],
					'country': loc['country']['long_name']}
		except:
			pass

	def get_resp_address(self):
		try:
			loc = self.get_address_components()
			return ", ".join([loc['street_number']['long_name'],
							  loc['route']['long_name'],
							  loc['postal_code']['long_name'],
							  loc['locality']['long_name'],
							  loc['country']['long_name']])
		except:
			return None


class empty(GeoLoc):

	def __init__(self, query):
		GeoLoc.__init__(self, query)
		self.locator = None
		self.properties = None

	def get_latitude(self):
		return np.nan

	def get_longitude(self):
		return np.nan

	def get_resp_address(self):
		return None
		
	def match_score(self):
		pass


if __name__ == '__main__':
	queries = ["148 rue de lourmel, 75015, Paris", '2923 rue whawha, 17019, Toutouville']
	#print("\nUsing OSM...")
	for query in queries:
		resp = osm(query)
		#print("Query: %s" % query)

		#print("Outputs:")
		# print("Locator", resp.locator)
		#print("Resp address: ", resp.get_resp_address())
		#print("properties: ", resp.properties)
		#print("Match score: ", resp.score)
		#print("Geometry: ", resp.geometry)
		#print("")

	#print("\nUsing Google...")
	for query in queries:
		resp = gg(query)
		#print("Query: %s" % query)

		#print("Outputs:")
		# print("Locator", resp.locator)
		#print("Resp address: ", resp.get_resp_address())
		#print("properties: ", resp.properties)
		#print("Match score: ", resp.score)
		#print("Geometry: ", resp.geometry)
		#print("")


