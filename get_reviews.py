import time
import ast
import multiprocessing as mp
from queue import Queue
from threading import Thread
import html

from connector import connector, get_connector
from util import sanitize_business_url, sanitize_review_object, sanitize_user_object
from constants import REVIEW_PATH
from requester import request_json
from logger import logger


class DownloadWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            try:
                business = self.queue.get()
                con1 = get_connector()
                try:
                    added = recursive_fetch(business, con1)
                    if added > 0:
                        logger.info('Added business: ' + business[0] + ' reviews: ' + str(business[1]) + ' counted: ' + str(added))
                        print('Added business: ' + business[0] + ' reviews: ' + str(business[1]) + ' counted: ' + str(added))
                finally:
                    self.queue.task_done()
            except:
                logger.exception("Error before processing")
                print("Error before processing")
            finally:
                con1.close()


def recursive_fetch(business, connector1):
	url = business[0]
	review_count = business[1]
	business_id = business[2]
	counted = business[3]

	if counted is None:
		counted = 0
	s_url = sanitize_business_url(url) + REVIEW_PATH
	try:
		while True:
			new_url = s_url + str(counted)
			response = request_json(new_url, '', with_token=False, with_proxy=True)
			# print(response)
			reviews = response['reviews']
			# print(str(review_count) + " " + str(response['pagination']['totalResults']))
			if review_count != response['pagination']['totalResults']:
				review_count = response['pagination']['totalResults']
				connector1.update_total_reviews(business_id, review_count)
			if len(reviews) == 0:
				break
			counted = counted + len(reviews)
			for review in reviews:
				# logger.info('Review: ' + str(review))
				connector1.enter_review_record(sanitize_review_object(review))
				user = review['user']
				# logger.info('User: ' + str(user))
				user['id'] = review['userId']
				connector1.enter_user_record(sanitize_user_object(user))
			# time.sleep(0.2)
			if counted >= review_count:
				break
	except:
		logger.error('Faced the following error for url ' + new_url)
		logger.exception('Error: ')
		print('Faced the following error for url ' + new_url)
		counted = counted * -1
	return counted


# # MultiProcessing setup
# def looper(businesses):
# 	i = 0
# 	logger.info("Partial Length: " + str(len(businesses)))
# 	print("Partial Length: " + str(len(businesses)))
# 	for business in businesses:
# 		added = recursive_fetch(business, connector)
# 		if added > 0:
# 			logger.info('Added business: ' + business[0] + ' reviews: ' + str(business[1]) + ' counted: ' + str(added))
# 			print('Added business: ' + business[0] + ' reviews: ' + str(business[1]) + ' counted: ' + str(added))
# 		i = i + 1
# 		# if i == 1:
# 		# 	break


def query_review_api():
	print("Number of processors: ", mp.cpu_count())
	bus_len = 1
	while bus_len > 0:
		try:
			businesses = connector.get_business_records_for_reviews()
		except:
			logger.error('Unable to fetch business records where reviews not logged. Trying to fetch all records.')
			try:
				businesses = connector.get_business_records()
			except:
				logger.error('Unable to fetch all businesses either. Cancelling operation.')
				print("Error")
				return

		bus_len = len(businesses)
		logger.info("Full Length: " + str(bus_len))
		print("Full Length: " + str(bus_len))

		# # Single threaded
		# i = 0
		# for business in businesses:
		# 	added = recursive_fetch(business, connector)
		# 	if added > 0:
		# 		logger.info('Added business: ' + business[0] + ' reviews: ' + str(business[1]) + ' counted: ' + str(added))
		# 		print('Added business: ' + business[0] + ' reviews: ' + str(business[1]) + ' counted: ' + str(added))
		# 	i = i + 1
		# 	# if i == 1:
		# 	# 	break

		# # Multiprocessing
		# pool = mp.Pool(2)
		# loop_bus = []
		# loop_bus.append(businesses[0:math.floor(bus_len / 2)])
		# loop_bus.append(businesses[math.floor(bus_len / 2):bus_len])
		# pool.map(looper, [itr_bus for itr_bus in loop_bus])
		# pool.close()

		# Multithreaded process
		# Create a queue to communicate with the worker threads
		try:
			queue = Queue()
			# Create 4 worker threads
			for x in range(5):
				worker = DownloadWorker(queue)
				# Setting daemon to True will let the main thread exit even though the workers are blocking
				worker.daemon = True
				worker.start()
			for business in businesses:
				# logger.info('Queueing {}'.format(business))
				queue.put((business))
			# Causes the main thread to wait for the queue to finish processing all the tasks
			queue.join()
		except:
			logger.exception("Error while running parallel threads")
			print("Error while running parallel threads")


def add_total_photos_for_reviews_backlog():
	try:
		reviews = connector.get_review_info_for_backlog()
	except Exception as e:
		logger.error('Unable to fetch review records.')
		logger.error("Error: " + str(e))
		print("Error")
		return

	logger.info("No of records found: " + str(len(reviews)))
	for review in reviews:
		try:
			total_photos = ast.literal_eval(review[1])['totalPhotos']
			# print(str(review[0]) + " " + str(total_photos))
			connector.add_total_photos(review[0], total_photos)
		except:
			logger.error("Faced an exception for review id: " + str(review[0]))
			logger.exception("Error: ")
			print("Error")


def decode_review_string():
	try:
		reviews = connector.get_reviews_for_html_decode()
	except Exception as e:
		logger.error('Unable to fetch review records.')
		logger.error("Error: " + str(e))
		print("Error")
		return

	# reviews = [(0, 'I&#39;m only giving two stars cause the place just opened but wow does this place deserve one star. Almost every single employee I&#39;ve interacted with has no clue what they&#39;re doing, they avoid customers because they don&#39;t know what to do with them. My wings never have nearly enough sauce, sometimes the foods even cold. Tonight I came for the boneless special, to find out they ran out of the boneless wings and I have to wait 40 min because they&#39;re out getting more boneless wings, then I find out they have to use chicken nuggets instead. Sigh. Wait is almost always more than half hour anytime after the evening. On nights with specials it&#39;s always over an hour. Hopefully it gets better.<br><br>Never mind, they just covered my whole meal plus dessert, and gave me 4 free wing coupons for my next visit. They felt really bad, maybe they just really messed up tonight. It is true they just opened.')]
	logger.info("No of records found: " + str(len(reviews)))
	for review in reviews:
		try:
			html_decoded_string = html.unescape(review[1]).replace('<br>', '').replace('<br/>', '').replace('</br>', '')
			# print(review[0])
			# print(review[1])
			# print(html_decoded_string)
			connector.update_reviews_for_html_decode(review[0], html_decoded_string)
		except:
			logger.error("Faced an exception for review id: " + str(review[0]))
			logger.exception("Error: ")
			print("Error")


if __name__ == '__main__':
	# add_total_photos_for_reviews_backlog()
	decode_review_string()
