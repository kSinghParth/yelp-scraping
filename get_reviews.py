import time

from connector import connector
from util import sanitize_business_url, sanitize_review_object, sanitize_user_object
from constants import REVIEW_PATH
from requester import request
from logger import logger


def recursive_fetch(url, review_count):
	counted = 0
	s_url = sanitize_business_url(url) + REVIEW_PATH
	try:
		while counted < review_count:
			new_url = s_url + str(counted)
			response = request(new_url, '', with_token=False)
			reviews = response['reviews']
			if len(reviews) == 0:
				break
			counted = counted + len(reviews)
			for review in reviews:
				connector.enter_review_record(sanitize_review_object(review))
				user = review['user']
				user['id'] = review['userId']
				connector.enter_user_record(sanitize_user_object(user))
			time.sleep(1)
	except Exception as e:
		logger.error('Faced the following error for url ' + new_url)
		logger.error('Error: ' + str(e))
		logger.error('Response: ' + str(response))
		logger.error('Review: ' + str(review))
		logger.error('User: ' + str(user))


def query_review_api():
	try:
		businesses = connector.get_business_records_for_reviews()
	except:
		logger.error('Unable to fetch business records where reviews not logged. Trying to fetch all records.')
		try:
			businesses = connector.get_business_records()
		except:
			logger.error('Unable to fetch all businesses either. Cancelling operation.')
			return

	for business in businesses:
		recursive_fetch(business[0], business[1])
