import ast
from bs4 import BeautifulSoup

from connector import connector
from logger import logger
from util import sanitize_image_object
from requester import generic_request
from constants import WEB_HOST


def populate_review_images_backlog():
	try:
		reviews = connector.get_review_photo_info()
	except:
		logger.error('Unable to fetch review records. Trying to fetch all records.')

	logger.info('Total reviews to be fixed: ' + str(len(reviews)))
	for review in reviews:
		try:
			review_id = review[0]
			image_date = review[3]
			total_photos = review[1]
			photos = ast.literal_eval(review[2])['photos']
			logger.info('Checking for review id: ' + review_id + ', total photos: ' + str(total_photos))
			if total_photos != len(photos):
				logger.info('Fetching from web')
				url = photos[0]['link'][0:photos[0]['link'].index('select=')]
				response = generic_request(WEB_HOST + url, '', url_params=None, with_token=False)
				page = response.content
				if response.status_code == 200:
					with open('a.html', 'wb') as f:
						f.write(page)
				soup = BeautifulSoup(page, 'html.parser')
				web_photos = soup.select('#super-container > div.container > div > div.media-landing.js-media-landing > div.media-landing_gallery.photos > ul > li > div')
				for web_photo in web_photos:
					photo = {}
					photo['id'] = web_photo['data-photo-id']
					photo['review_id'] = review_id
					photo['image_url'] = web_photo.img['src']
					photo['src_set'] = web_photo.img['srcset']
					photo['height'] = web_photo.img['height']
					photo['width'] = web_photo.img['width']
					photo['alt_text'] = web_photo.img['alt']
					photo['web_url'] = WEB_HOST + web_photo.a['href']
					photo['image_date'] = image_date
					photo['caption'] = None
					connector.enter_photo_record(photo)
			else:
				logger.info('Not fetching from web')
				for photo in photos:
					photo['reviewId'] = review_id
					photo['imageDate'] = image_date
					connector.enter_photo_record(sanitize_image_object(photo))
			print("Successful image population for review: " + review_id)
			logger.info("Successful image population for review: " + review_id)
		except Exception as e:
			logger.error("Error while saving image for review id: " + review_id)
			logger.error("Error: " + str(e))
			print("Error while saving image for review id: " + review_id)
