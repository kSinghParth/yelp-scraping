import logging
import datetime

logger = logging
logger.basicConfig(
	filename='logs/yelp_scapper_' + str(datetime.datetime.now()) + '.log',
	filemode='w',
	format='%(asctime)s - %(levelname)s - %(funcName)s(%(lineno)s)  : %(message)s',
	level=logging.INFO)
