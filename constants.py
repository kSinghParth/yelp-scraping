# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
WEB_HOST = 'https://www.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
REVIEW_PATH = '/review_feed?rl=en&sort_by=relevance_desc&q=&start='


# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'Los Angeles, CA'
SEARCH_LIMIT = 50
# Radius Limit in km
RADIUS_LIMIT = 40


coordinates = [
	# # LA coordinates
	# {'north_lat': 33.799846, 'east_lng': -118.233804, 'south_lat': 33.718122, 'west_lng': -118.318322},
	# {'north_lat': 34.010706, 'east_lng': -118.227156, 'south_lat': 33.940070, 'west_lng': -118.318485},
	# {'north_lat': 34.103051, 'east_lng': -118.354037, 'south_lat': 33.932200, 'west_lng': -118.455767},
	# {'north_lat': 34.152330, 'east_lng': -118.182790, 'south_lat': 34.011307, 'west_lng': -118.337423},
	# {'north_lat': 34.322895, 'east_lng': -118.334684, 'south_lat': 34.067079, 'west_lng': -118.592686},

	# # NY coordinates
	# {'north_lat': 40.647256, 'east_lng': -74.060387, 'south_lat': 40.493197, 'west_lng': -74.263548},
	# {'north_lat': 40.893144, 'east_lng': -73.728518, 'south_lat': 40.563087, 'west_lng': -74.035190},

	# # Chicago coordinates
	# {'north_lat': 42.039240, 'east_lng': -87.526003, 'south_lat': 41.658200, 'west_lng': -87.808192},
	# {'north_lat': 42.015493, 'east_lng': -87.842098, 'south_lat': 41.945851, 'west_lng': -87.936967},

	# # Houston
	# {'north_lat': 30.113427, 'east_lng': -95.093830, 'south_lat': 29.512591, 'west_lng': -95.629297},

	# # Phoenix
	# {'north_lat': 33.936155, 'east_lng': -111.923215, 'south_lat': 33.294580, 'west_lng': -112.289884},

	# # Philly
	# {'north_lat': 40.086519, 'east_lng': -75.107737, 'south_lat': 39.872372, 'west_lng': -75.264979},
	# {'north_lat': 40.136932, 'east_lng': -74.967662, 'south_lat': 39.964006, 'west_lng': -75.126277},

	# # San Antonio
	# {'north_lat': 29.678058, 'east_lng': -98.300183, 'south_lat': 29.214056, 'west_lng': -98.675091},

	# # San Diego
	# {'north_lat': 33.040564, 'east_lng': -117.062797, 'south_lat': 32.525442, 'west_lng': -117.279174},

	# # San Diego
	# {'north_lat': 33.040564, 'east_lng': -117.062797, 'south_lat': 32.525442, 'west_lng': -117.279174},

	# # Dallas
	# {'north_lat': 32.927851, 'east_lng': -96.634058, 'south_lat': 32.643580, 'west_lng': -96.921328},

	# # San Jose
	# {'north_lat': 37.456655, 'east_lng': -121.743264, 'south_lat': 37.189642, 'west_lng': -122.007622},

	# # Austin
	# {'north_lat': 30.508439, 'east_lng': -97.599602, 'south_lat': 30.136811, 'west_lng': -97.937432},

	# # Jacksonville
	# {'north_lat': 30.511655, 'east_lng': -81.386514, 'south_lat': 30.107374, 'west_lng': -81.846566},

	# # Fort Worth
	# {'north_lat': 33.039127, 'east_lng': -97.249530, 'south_lat': 32.551973, 'west_lng': -97.496722},

	# # Columbus
	# {'north_lat': 40.159419, 'east_lng': -82.780724, 'south_lat': 39.859114, 'west_lng': -83.163872},

	# # Indianapolis
	# {'north_lat': 40.077340, 'east_lng': -85.936643, 'south_lat': 39.629143, 'west_lng': -86.324332},

	# # Charlotte
	# {'north_lat': 35.393052, 'east_lng': -80.683283, 'south_lat': 35.030080, 'west_lng': -80.990213},

	# # SF
	# {'north_lat': 37.832559, 'east_lng': -122.364598, 'south_lat': 37.707049, 'west_lng': -122.510809},

	# # Seattle
	# {'north_lat': 47.740084, 'east_lng': -122.255555, 'south_lat': 47.494772, 'west_lng': -122.410737},

	# # Denver
	# {'north_lat': 39.800137, 'east_lng': -104.863360, 'south_lat': 39.646981, 'west_lng': -105.055620},

	# # Washington DC
	# {'north_lat': 38.997575, 'east_lng':  -76.927957, 'south_lat': 38.854977, 'west_lng': -77.094229},
	
	# # Nashville
	# {'north_lat': 36.410440, 'east_lng':  -86.529849, 'south_lat': 35.939866, 'west_lng': -86.974795},
	
	# # Oklahoma
	# {'north_lat': 35.716816, 'east_lng':  -97.151016, 'south_lat': 35.268452, 'west_lng': -97.812943},
	
	# # El paso
	# {'north_lat': 32.001317, 'east_lng':  -106.232925, 'south_lat': 31.630577, 'west_lng': -106.621594},

	# # Portland
	# {'north_lat': 45.652169, 'east_lng':  -122.493047, 'south_lat': 45.420826, 'west_lng': -122.821264},

	# # Las vegas
	# {'north_lat': 36.335339, 'east_lng':  -115.069215, 'south_lat': 36.130465, 'west_lng': -115.351477},

	# # Detroit
	# {'north_lat': 42.452005, 'east_lng':  -82.908326, 'south_lat': 42.251564, 'west_lng': -83.273621},

	# # Memphis
	# {'north_lat': 38.362294, 'east_lng':  -85.435767, 'south_lat': 38.047391, 'west_lng': -85.922358},

	# # Baltimore
	# {'north_lat': 39.372070, 'east_lng':  -76.529757, 'south_lat': 39.211522, 'west_lng': -76.703526},

	# # Milwaukee
	# {'north_lat': 43.192116, 'east_lng':  -87.876114, 'south_lat': 42.923704, 'west_lng': -88.058075},

	# # Albuquerque
	# {'north_lat': 35.216159, 'east_lng':  -106.477372, 'south_lat': 34.947925, 'west_lng': -106.756139},

	# # Tucson
	# {'north_lat': 32.298724, 'east_lng':  -110.745798, 'south_lat': 32.081976, 'west_lng': -111.033503},

	# Fresno
	{'north_lat': 36.911006, 'east_lng':  -119.677154, 'south_lat': 36.685841, 'west_lng': -119.927033},

	# Sacramento
	{'north_lat': 38.676458, 'east_lng':  -121.367390, 'south_lat': 38.439668, 'west_lng': -121.552098},

	# Kansas City
	{'north_lat': 39.327809, 'east_lng':  -94.380746, 'south_lat': 38.839857, 'west_lng': -94.689634},

	# Mesa
	{'north_lat': 33.508283, 'east_lng':  -111.576406, 'south_lat': 33.270955, 'west_lng': -111.892708},

	# Atlanta
	{'north_lat': 33.893918, 'east_lng':  -84.291301, 'south_lat': 33.656826, 'west_lng': -84.542836},

	# Omaha
	{'north_lat': 41.364028, 'east_lng':  -95.910120, 'south_lat': 41.190059, 'west_lng': -96.292744},

	# Colordado Springs
	{'north_lat': 39.032054, 'east_lng':  -104.637518, 'south_lat': 38.727373, 'west_lng': -104.904623},

	# Raleigh
	{'north_lat': 35.972159, 'east_lng':  -78.510482, 'south_lat': 35.720024, 'west_lng': -78.779647},

	# Long beach
	{'north_lat': 33.888438, 'east_lng':  -118.080054, 'south_lat': 33.736258, 'west_lng': -118.229926},

	# Virginia Beach
	{'north_lat': 36.935572, 'east_lng':  -75.959141, 'south_lat': 36.689697, 'west_lng': -76.189818},

	# # Miami
	# {'north_lat': 25.859343, 'east_lng':  -80.149123, 'south_lat': 25.708644, 'west_lng': -80.262704},

	# # Oakland
	# {'north_lat': 37.856916, 'east_lng':  -122.153812, 'south_lat': 37.723340, 'west_lng': -122.317027},

	# # Minneapolis
	# {'north_lat': 45.051744, 'east_lng':  -93.206892, 'south_lat': 44.889979, 'west_lng': -93.322249},

	# # Tulsa
	# {'north_lat': 36.244982, 'east_lng':  -95.692295, 'south_lat': 36.000158, 'west_lng': -96.060667},

	# # Bakersfield
	# {'north_lat': 35.424503, 'east_lng':  -118.935124, 'south_lat': 35.263730, 'west_lng': -119.149158},

	# # Wichita
	# {'north_lat': 37.792150, 'east_lng': -97.154571, 'south_lat': 37.570977, 'west_lng': -97.524673},

	# # Arlington
	# {'north_lat': 32.814367, 'east_lng': -97.039292, 'south_lat': 32.598278, 'west_lng': -97.230179},
]


cities = ['Boston', 'New York', 'Philadelphia', 'Washington', 'Baltimore', 'Virginia Beach', 'Raleigh', 'Charlotte', 'Atlanta', 'Jacksonville', 'Miami', 'Nashville', 'Memphis', 'Louisville', 'Columbus', 'Indianapolis', 'Detroit', 'Milwaukee', 'Minneapolis', 'Chicago', 'Kansas City', 'Wichita', 'Omaha', 'Oklahoma City', 'Austin', 'Tulsa', 'Dallas', 'Arlington', 'Fort Worth', 'Houston', 'San Antonio', 'El Paso', 'Denver', 'Colorado Springs', 'Phoenix', 'Mesa', 'Tucson', 'Albuquerque', 'Las Vegas', 'Los Angeles', 'Long Beach', 'San Diego', 'Bakersfield', 'Fresno', 'San Francisco', 'Sacramento', 'Oakland', 'San Jose', 'Portland', 'Seattle']
