import argparse
import json
import sys
import urllib
import math

from constants import *
from connector import Connector
from requester import *
from util import *
from logger import logger

connector = None

def search(term=None, location=None, latitude=None, longitude=None, radius=None):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'limit': SEARCH_LIMIT
    }
    if latitude:
        url_params['latitude']= latitude
    if longitude:
        url_params['longitude']= longitude
    if radius:
        url_params['radius']= radius
    if term:
        url_params['term']= term
    if location:
        url_params['location']= location
    
    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def recursive_search(coordinates, level):
    # logging.info(coordinates)
    n_l = coordinates['north_lat']
    s_l = coordinates['south_lat']
    e_l = coordinates['east_lng']
    w_l = coordinates['west_lng']
    mid_lat = (n_l + s_l)/2
    mid_lng = (e_l + w_l)/2
    radius = distance_calc(coordinates)/2.0
    logger.info("Coordinates: " + str(coordinates))
    logger.info("Centre: " + str(mid_lat) + "," + str(mid_lng))
    logger.info("Radius is : " + str(radius))

    if connector.does_coordinate_record_exist(mid_lat, mid_lng, radius):
        logger.info("Coordinate record exists. Skipping");
        return

    if(radius<50):
        return

    response = search(latitude = mid_lat, longitude = mid_lng, radius = int(math.ceil(radius*1000)))
    # logging.info(response)
    businesses = response.get('businesses')
    
    if businesses:
        logger.info("Businesses count: " +  str(len(businesses)))
        for business in businesses:
            if business_in_US(business):
                connector.enter_business_record(sanitize_business_object(business))
        
        recur_crdnts = []
        if len(businesses) >= 50:
            recur_crdnts.append({'north_lat': n_l, 'east_lng': e_l, 'south_lat': mid_lat,'west_lng': mid_lng})
            recur_crdnts.append({'north_lat': mid_lat, 'east_lng': mid_lng, 'south_lat': s_l,'west_lng': w_l})
            recur_crdnts.append({'north_lat': n_l, 'east_lng': mid_lng, 'south_lat': mid_lat,'west_lng': w_l})
            recur_crdnts.append({'north_lat': mid_lat, 'east_lng': e_l, 'south_lat': s_l,'west_lng': mid_lng})

            for crdnt in recur_crdnts:
                 recursive_search(crdnt, level + 1)
    else:
        logger.info(u'No businesses found for lat, lng: {0}, {1}'.format(mid_lat, mid_lng))
        logger.info('Error: ' + response)
        businesses = []
    
    connector.enter_coordinate_record(mid_lat, mid_lng, radius, n_l, s_l, e_l, w_l, len(businesses), level)

def get_business( business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)


def query_api(term=None, location=None, coordinates=None):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """

    if coordinates:
        temp_crdnt = coordinates.copy()
        while len(temp_crdnt) > 0:
            logger.info("Current coordinates array: " + str(temp_crdnt))
            crdnt = temp_crdnt.pop()
            if is_valid_distance(crdnt, RADIUS_LIMIT):
                logger.info("Radius is Okay. " + coordinate_string(crdnt))
                response = recursive_search(coordinates = crdnt, level = 1)
            else:
                logger.info("Radius more than limit. " + coordinate_string(crdnt))
                n_l = crdnt['north_lat']
                s_l = crdnt['south_lat']
                e_l = crdnt['east_lng']
                w_l = crdnt['west_lng']
                mid_lat = (n_l + s_l)/2.0
                mid_lng = (e_l + w_l)/2.0
                temp_crdnt.append({'north_lat': n_l, 'east_lng': e_l, 'south_lat': mid_lat,'west_lng': mid_lng})
                temp_crdnt.append({'north_lat': mid_lat, 'east_lng': mid_lng, 'south_lat': s_l,'west_lng': w_l})
                temp_crdnt.append({'north_lat': n_l, 'east_lng': mid_lng, 'south_lat': mid_lat,'west_lng': w_l})
                temp_crdnt.append({'north_lat': mid_lat, 'east_lng': e_l, 'south_lat': s_l,'west_lng': mid_lng})
        
    else:
        response = search( term, location)

    

    # business_id = 'RVbZaawgEGmto6TxOoVBdQ'
    # response = get_business(API_KEY, business_id)
    # logging.info(response)



def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        # query_api(input_values.term, input_values.location)
        query_api(None, None, coordinates)

    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    connector = Connector()
    main()