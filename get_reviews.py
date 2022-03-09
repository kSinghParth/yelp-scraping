import time
import ast

from connector import connector
from util import sanitize_business_url, sanitize_review_object, sanitize_user_object
from constants import REVIEW_PATH
from requester import request_json
from logger import logger


def recursive_fetch(url, review_count):
	counted = 0
	s_url = sanitize_business_url(url) + REVIEW_PATH
	try:
		while counted < review_count:
			new_url = s_url + str(counted)
			response = request_json(new_url, '', with_token=False)
			reviews = response['reviews']
			if len(reviews) == 0:
				break
			counted = counted + len(reviews)
			for review in reviews:
				logger.info('Review: ' + str(review))
				connector.enter_review_record(sanitize_review_object(review))
				user = review['user']
				logger.info('User: ' + str(user))
				user['id'] = review['userId']
				connector.enter_user_record(sanitize_user_object(user))
			# time.sleep(0.5)
	except:
		logger.error('Faced the following error for url ' + new_url)
		logger.exception('Error: ')
		print('Faced the following error for url ' + new_url)


def query_review_api():
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

	i = 0
	logger.info("Length: " + str(len(businesses)))
	for business in businesses:
		recursive_fetch(business[0], business[1])
		logger.info('Added business: ' + business[0] + ' reviews: ' + str(business[1]))
		print('Added business: ' + business[0] + ' reviews: ' + str(business[1]))
		i = i + 1
		if i == 5:
			break


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


if __name__ == '__main__':
	add_total_photos_for_reviews_backlog()
