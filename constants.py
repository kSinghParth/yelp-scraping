# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'


# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'Los Angeles, CA'
SEARCH_LIMIT = 50
# Radius Limit in km
RADIUS_LIMIT = 40


coordinates = [

		{'north_lat': 33.799846, 'east_lng': -118.233804, 
		'south_lat': 33.718122,'west_lng': -118.318322},

		{'north_lat': 34.010706, 'east_lng': -118.227156, 
		'south_lat': 33.940070,'west_lng': -118.318485},

		{'north_lat': 34.103051, 'east_lng': -118.354037, 
		'south_lat': 33.932200,'west_lng': -118.455767},

		{'north_lat': 34.152330, 'east_lng': -118.182790, 
		'south_lat': 34.011307,'west_lng': -118.337423},

		{'north_lat': 34.322895, 'east_lng': -118.334684, 
		'south_lat': 34.067079,'west_lng': -118.592686},
	]