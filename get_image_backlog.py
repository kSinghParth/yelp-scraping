import ast
from bs4 import BeautifulSoup
from threading import Thread
from queue import Queue

from connector import get_connector, connector
from logger import logger
from util import sanitize_image_object
from requester import generic_request
from constants import WEB_HOST


class DownloadWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            try:
                review = self.queue.get()
                con1 = get_connector()
                try:
                    fetch_images(review, con1)
                finally:
                    self.queue.task_done()
            except:
                logger.exception("Error before processing")
                print("Error before processing")
            finally:
                con1.close()


def fetch_images(review, con1):
	try:
		review_id = review[0]
		image_date = review[3]
		total_photos = review[1]
		photos = ast.literal_eval(review[2])['photos']
		logger.info('Checking for review id: ' + review_id + ', total photos: ' + str(total_photos))

		if total_photos != len(photos):
			logger.info('Fetching from web')
			ct = 0
			while ct < total_photos:
				url = photos[0]['link'][0:photos[0]['link'].index('select=')] + 'start=' + str(ct)
				response = generic_request(WEB_HOST + url, '', url_params=None, with_token=False, with_proxy=True)
				page = response.content
				if response.status_code == 200:
					with open('a.html', 'wb') as f:
						f.write(page)
				else:
					break
				soup = BeautifulSoup(page, 'html.parser')
				web_photos = soup.select('#super-container > div.container > div > div.media-landing.js-media-landing > div.media-landing_gallery.photos > ul > li > div')
				logger.info("no of images: " + str(len(web_photos)))
				tmp_ct = 0
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
					con1.enter_photo_record(photo)
					tmp_ct = tmp_ct + 1
				logger.info("Added: " + str(tmp_ct))
				print("Added: " + str(tmp_ct))
				if tmp_ct <= 30:
					break
				ct = ct + tmp_ct
		else:
			logger.info('Not fetching from web')
			for photo in photos:
				photo['reviewId'] = review_id
				photo['imageDate'] = image_date
				con1.enter_photo_record(sanitize_image_object(photo))
		print("Successful image population for review: " + review_id)
		logger.info("Successful image population for review: " + review_id)
	except Exception:
		logger.error("Error while saving image for review id: " + review_id)
		logger.error(web_photo)
		logger.exception("Error: ")
		print("Error while saving image for review id: " + review_id)


def populate_review_images_backlog():
	try:
		reviews = connector.get_review_photo_info()
	except:
		logger.error('Unable to fetch review records. Trying to fetch all records.')

	print("reached here in image")
	logger.info('Total reviews to be fixed: ' + str(len(reviews)))
	try:
		queue = Queue()
		# Create 4 worker threads
		for x in range(30):
			worker = DownloadWorker(queue)
			# Setting daemon to True will let the main thread exit even though the workers are blocking
			worker.daemon = True
			worker.start()
		for review in reviews:
			# logger.info('Queueing {}'.format(business))
			queue.put((review))
		# Causes the main thread to wait for the queue to finish processing all the tasks
		queue.join()
	except:
		logger.exception("Error while running parallel threads")
		print("Error while running parallel threads")
