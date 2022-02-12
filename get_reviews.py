import time

from connector import connector
from util import sanitize_business_url, sanitize_review_object, sanitize_user_object
from constants import REVIEW_PATH
from requester import request


def recursive_fetch(url, review_count):
	counted = 0
	s_url = sanitize_business_url(url) + REVIEW_PATH
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


def query_review_api():
	businesses = connector.get_business_records()
	for business in businesses:
		recursive_fetch(business[0], business[1])
