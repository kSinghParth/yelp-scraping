import argparse

from requester import *
from constants import coordinates
from logger import logger
from get_business import query_business_api_by_coordinate, populate_zip, query_business_api_by_zip
from get_reviews import query_review_api
from get_image_backlog import populate_review_images_backlog

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
    parser.add_argument('-ib', '--image-backlog', dest='imagebklg', default=False,
                        action="store_true", help='Store image backlog (Default:False')
    parser.add_argument('-c', '--city', dest='city', help='City to pick zip code of')
    parser.add_argument('-s', '--state', dest='state', help='City to pick zip code of')

    input_values = parser.parse_args()

    if input_values.city is not None and input_values.state is not None:
        populate_zip(input_values.city, input_values.state)

    try:
        if input_values.businesses:
            logger.info("Fetching businesses")
            query_business_api_by_coordinate(None, None, coordinates)
            # query_business_api_by_zip()
        if input_values.reviews:
            logger.info("Fetching reviews")
            query_review_api()
        if input_values.imagebklg:
            logger.info("Populating image backlog")
            populate_review_images_backlog()

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
