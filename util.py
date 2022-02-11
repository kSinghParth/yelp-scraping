from datetime import datetime
from geopy import distance
from logger import logger

def sanitize_str(unsanitized_str):
	return str(unsanitized_str or '')

def sanitize_address_str(business):
	res = ''

	try:
		res = res + sanitize_str(business['location']['address1']) 
	except:
		pass
	try:
		if business['location']['address2'] and len(business['location']['address2'])>0:
			res = res + ' | ' + business['location']['address2']
	except:
		pass

	try:
		if business['location']['address3'] and len(business['location']['address3'])>0:
			res = res + ' | ' + business['location']['address3']
	except:
		pass

	return res

def santize_business_object(business):
	try:
		business_id = business['id']
	except:
		# generate random id
		business_id = 'xxxxx' + datetime.now().timestamp()
	try:
		name = business['name']
	except:
		name = None
	try:
		review_count = business['review_count']
	except:
		review_count = None
	try:
		rating = business['rating']
	except:
		rating = None
	try:
		zip_code = business['location']['zip_code']
	except:
		zip_code = None
	try:
		city = business['location']['city']
	except:
		city = None
	try:
		state = business['location']['state']
	except:
		state = None
	try:
		country = business['location']['country']
	except:
		country = None	
	try:
		url = business['url']
	except:
		url = None
	try:
		latitude = business['coordinates']['latitude']
	except:
		latitude = None
	try:
		longitude = business['coordinates']['longitude']
	except:
		longitude = None
	try:
		price = business['price']
	except:
		price = None
	try:
		price = business['price']
	except:
		price = None
	try:
		is_open = not business['is_closed']
	except:
		is_open = None
	try:
		phone = business['phone']
	except:
		phone = None
	try:
		categories_str = ', '.join(x['title'] for x in business['categories'])
	except:
		categories_str = None
	try:
		alias = business['alias']
	except:
		alias = None
	try:
		image_url = business['image_url']
	except:
		image_url = None
	try:
		transactions_str = ', '.join(x for x in business['transactions'])
	except:
		transactions_str = None

	address = sanitize_address_str(business)
	
	return {'id': business_id, 
		'name': name, 
		'review_count': review_count, 
        'rating': rating, 
        'zip_code': zip_code, 
        'city': city, 
        'state': state,
        'country': country, 
        'url': url,
        'latitude': latitude, 
        'longitude': longitude,
        'address': address, 
        'price': price, 
        'open': is_open,
        'phone': phone, 
        'categories_str': categories_str, 
        'alias': alias,
        'image_url': image_url,
        'transactions_str': transactions_str
        }


def distance_calc(coordinates):

	n_l = coordinates['north_lat']
	s_l = coordinates['south_lat']
	e_l = coordinates['east_lng']
	w_l = coordinates['west_lng']
	coords_1 = (n_l, e_l)
	coords_2 = (s_l, w_l)

	dist = distance.distance(coords_1, coords_2).km
	logger.info("Radius is {} for coordinates: {}".format(dist, coordinate_string(coordinates)))
	return dist

def is_valid_distance(coordinates, valid_radius_limit):
	if distance_calc(coordinates)/2.0 > valid_radius_limit:
		return False
	else:
		return True

def coordinate_string(coordinate):
    return "North Latitude: "+str(coordinate['north_lat'])+'  , South Latitude: '+str(coordinate['south_lat'])+'  , East Longitude: '+str(coordinate['east_lng'])+'  , West Longitude: '+str(coordinate['west_lng'])

def business_in_US(business):
	if business['location']['country']=='US':
		return True
	return False;
