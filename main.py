import argparse

from requester import *
from constants import coordinates
from logger import logger
from get_business import query_business_api
from get_reviews import query_review_api

# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import urlencode


connector = None


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--businesses', dest='businesses', default=False,
                        action="store_true", help='Fetch businesses (Default:False)')
    parser.add_argument('-r', '--reviews', dest='reviews', default=False,
                        action="store_true", help='Fetch reviews (Default:False')

    input_values = parser.parse_args()

    try:
        if input_values.businesses:
            logger.info("Fetching businesses")
            query_business_api(None, None, coordinates)
        if input_values.reviews:
            logger.info("Fetching reviews")
            query_review_api()

    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()
