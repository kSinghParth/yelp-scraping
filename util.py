from datetime import datetime
from geopy import distance
from logger import logger
from constants import WEB_HOST, cities
import html

def sanitize_str(unsanitized_str):
	return str(unsanitized_str or '')


def sanitize_address_str(business):
	res = ''

	try:
		res = res + sanitize_str(business['location']['address1'])
	except:
		logger.debug("Address1 not found")

	try:
		if business['location']['address2'] and len(business['location']['address2']) > 0:
			res = res + ' | ' + business['location']['address2']
	except:
		logger.debug("Address1 not found")

	try:
		if business['location']['address3'] and len(business['location']['address3']) > 0:
			res = res + ' | ' + business['location']['address3']
	except:
		pass

	return res


def sanitize_business_object(business):
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

	return {
		'id': business_id,
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


def sanitize_review_object(review):

	try:
		review_id = review['id']
	except:
		# generate random id
		review_id = 'xxxxx' + datetime.now().timestamp()
	try:
		business_id = review['business']['id']
	except:
		business_id = None
	try:
		user_id = review['userId']
	except:
		user_id = None
	try:
		review_text = html.unescape(review['comment']['text']).replace('<br>', '').replace('<br/>', '').replace('</br>', '')
	except Exception as e:
		print("Error " + e)
		review_text = None
	try:
		rating = review['rating']
	except:
		rating = None
	try:
		language = review['comment']['language']
	except:
		language = None
	try:
		local_date = datetime.strptime(review['localizedDate'], '%m/%d/%Y')
	except:
		local_date = None
	try:
		useful = review['feedback']['counts']['useful']
	except:
		useful = None
	try:
		cool = review['feedback']['counts']['cool']
	except:
		cool = None
	try:
		funny = review['feedback']['counts']['funny']
	except:
		funny = None
	try:
		total_photos = review['totalPhotos']
	except:
		total_photos = None
	try:
		photos_url = WEB_HOST + review['photosUrl']
	except:
		photos_url = None

	return {
		'id': review_id,
		'business_id': business_id,
		'user_id': user_id,
		'review_text': review_text,
		'rating': rating,
		'language': language,
		'local_date': local_date,
		'useful': useful,
		'cool': cool,
		'funny': funny,
		'response_body': str(review),
		'total_photos': total_photos,
		'photos_url': photos_url

	}


def sanitize_user_object(user):
	# print(user)
	try:
		user_id = user['id']
	except:
		# generate random id
		user_id = 'xxxxx' + datetime.now().timestamp()
	try:
		review_count = user['reviewCount']
	except:
		review_count = None
	try:
		friend_count = user['friendCount']
	except:
		friend_count = None
	try:
		photo_count = user['photoCount']
	except:
		photo_count = None
	try:
		user_name = user['markupDisplayName']
	except:
		user_name = None
	try:
		useful = user['feedback']['counts']['useful']
	except:
		useful = None
	try:
		cool = user['feedback']['counts']['cool']
	except:
		cool = None
	try:
		funny = user['feedback']['counts']['funny']
	except:
		funny = None
	try:
		link = user['link']
	except:
		link = None
	try:
		user_url = user['userUrl']
	except:
		user_url = None
	try:
		elite_year = user['eliteYear']
	except:
		elite_year = None
	try:
		display_location = user['displayLocation']
	except:
		display_location = None
	try:
		src = user['src']
	except:
		src = None
	try:
		src_set = user['srcSet']
	except:
		src_set = None

	return {
		'id': user_id,
		'review_count': review_count,
		'friend_count': friend_count,
		'photo_count': photo_count,
		'user_name': user_name,
		'useful': useful,
		'cool': cool,
		'funny': funny,
		'link': link,
		'user_url': user_url,
		'elite_year': elite_year,
		'display_location': display_location,
		'src': src,
		'src_set': src_set
	}


def sanitize_image_object(photo):
	# print(user)
	try:
		image_id = photo['link'][photo['link'].index('select=') + 7:]
	except:
		# generate random id
		image_id = 'xxxxx' + datetime.now().timestamp()
	try:
		caption = photo['caption']
	except:
		caption = None
	try:
		review_id = photo['reviewId']
	except:
		review_id = None
	try:
		image_url = photo['src']
	except:
		image_url = None
	try:
		alt_text = photo['altText']
	except:
		alt_text = None
	try:
		web_url = WEB_HOST + photo['link']
	except:
		web_url = None
	try:
		width = photo['width']
	except:
		width = None
	try:
		height = photo['height']
	except:
		height = None
	try:
		# image_date = datetime.strptime(photo['imageDate'], '%m/%d/%Y')
		image_date = photo['imageDate']
	except:
		image_date = None
	try:
		src_set = photo['srcset']
	except:
		src_set = None

	return {
		'id': image_id,
		'review_id': review_id,
		'caption': caption,
		'image_url': image_url,
		'web_url': web_url,
		'alt_text': alt_text,
		'width': width,
		'height': height,
		'image_date': image_date,
		'src_set': src_set
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
	if distance_calc(coordinates) / 2.0 > valid_radius_limit:
		return False
	else:
		return True


def coordinate_string(coordinate):
	return 'North Latitude: ' + str(coordinate['north_lat']) + \
		'  , South Latitude: ' + str(coordinate['south_lat']) + \
		'  , East Longitude: ' + str(coordinate['east_lng']) + \
		'  , West Longitude: ' + str(coordinate['west_lng'])


def business_in_US(business):
	if business['location']['country'] == 'US':
		return True
	return False


def business_in_select_city(business):
	if business['location']['city'] in cities:
		return True
	return False


def sanitize_business_url(url):
	return url[0:url.index('?')]
