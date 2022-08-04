import math
# import json
import csv

from connector import connector
from constants import *
from util import *
from logger import logger
from requester import request_json


def populate_zip(city, state):
    logger.info("Populating Zip Codes")
    with open("zip_code_database.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[3] == city and row[4] == state:
                connector.enter_zip_code(row[0], city, state)

    logger.info("Populated Zip Codes")
    print("Populated Zip Codes")


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
        url_params['latitude'] = latitude
    if longitude:
        url_params['longitude'] = longitude
    if radius:
        url_params['radius'] = radius
    if term:
        url_params['term'] = term
    if location:
        url_params['location'] = location

    return request_json(API_HOST, SEARCH_PATH, url_params=url_params, with_token=True, with_proxy=False)


def recursive_search(coordinates, level):
    # logging.info(coordinates)
    n_l = coordinates['north_lat']
    s_l = coordinates['south_lat']
    e_l = coordinates['east_lng']
    w_l = coordinates['west_lng']
    mid_lat = (n_l + s_l) / 2
    mid_lng = (e_l + w_l) / 2
    radius = distance_calc(coordinates) / 2.0
    logger.info("Coordinates: " + str(coordinates))
    logger.info("Centre: " + str(mid_lat) + "," + str(mid_lng))
    logger.info("Radius is : " + str(radius))

    if connector.does_coordinate_record_exist(mid_lat, mid_lng, radius):
        logger.info("Coordinate record exists. Skipping")
        return

    if(radius * 1000 < 20):
        return

    response = search(latitude=mid_lat, longitude=mid_lng, radius=int(math.ceil(radius * 1000)))
    # logging.info(response)
    businesses = response.get('businesses')

    if businesses:
        logger.info("Businesses count: " + str(len(businesses)))
        for business in businesses:
            if business_in_select_city(business):
                try:
                    connector.enter_business_record(sanitize_business_object(business))
                except Exception as e:
                    print(e)
                    logger.exception("the error: ")
                    raise e

        recur_crdnts = []
        if len(businesses) >= 50:
            recur_crdnts.append(
                {'north_lat': n_l, 'east_lng': e_l, 'south_lat': mid_lat, 'west_lng': mid_lng}
            )
            recur_crdnts.append(
                {'north_lat': mid_lat, 'east_lng': mid_lng, 'south_lat': s_l, 'west_lng': w_l}
            )
            recur_crdnts.append(
                {'north_lat': n_l, 'east_lng': mid_lng, 'south_lat': mid_lat, 'west_lng': w_l}
            )
            recur_crdnts.append(
                {'north_lat': mid_lat, 'east_lng': e_l, 'south_lat': s_l, 'west_lng': mid_lng}
            )

            for crdnt in recur_crdnts:
                recursive_search(crdnt, level + 1)
    else:
        logger.info(u'No businesses found for lat, lng: {0}, {1}'.format(mid_lat, mid_lng))
        logger.info('Error: ' + str(response))
        businesses = []

    connector.enter_coordinate_record(
        mid_lat, mid_lng, radius, n_l, s_l, e_l, w_l, len(businesses), level)


def get_business(business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)


def query_business_api_by_coordinate(term=None, location=None, coordinates=None):
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
                response = recursive_search(coordinates=crdnt, level=1)
            else:
                logger.info("Radius more than limit. " + coordinate_string(crdnt))
                n_l = crdnt['north_lat']
                s_l = crdnt['south_lat']
                e_l = crdnt['east_lng']
                w_l = crdnt['west_lng']
                mid_lat = (n_l + s_l) / 2.0
                mid_lng = (e_l + w_l) / 2.0
                temp_crdnt.append(
                    {'north_lat': n_l, 'east_lng': e_l, 'south_lat': mid_lat, 'west_lng': mid_lng}
                )
                temp_crdnt.append(
                    {'north_lat': mid_lat, 'east_lng': mid_lng, 'south_lat': s_l, 'west_lng': w_l}
                )
                temp_crdnt.append(
                    {'north_lat': n_l, 'east_lng': mid_lng, 'south_lat': mid_lat, 'west_lng': w_l}
                )
                temp_crdnt.append(
                    {'north_lat': mid_lat, 'east_lng': e_l, 'south_lat': s_l, 'west_lng': mid_lng}
                )

    else:
        response = search(term, location)
        logger.info("Response: " + response)

    # business_id = 'RVbZaawgEGmto6TxOoVBdQ'
    # response = get_business(business_id)
    # logging.info(response)


def query_business_api_by_zip():
    """Queries the API by the zip code stored in the db.
    """
    zip_codes = connector.get_zip_codes()

    for zip in zip_codes:
        logger.info("Searching zip " + str(zip[0]) + " total:" + str(zip[3]) + " checked: " + str(zip[4]))
        print("Searching zip " + str(zip[0]) + " total:" + str(zip[3]) + " checked: " + str(zip[4]))
        recursive_search_by_zip(zip[0], zip[3], zip[4])


def recursive_search_by_zip(zip, total, checked):
    if checked is None:
        checked = 0
    if total is None:
        total = 1
    i = 0
    try:
        while total > checked:
            url_params = {
                'limit': SEARCH_LIMIT
            }
            url_params['offset'] = checked
            url_params['location'] = ("0" + str(zip))[-5:]
            response = request_json(API_HOST, SEARCH_PATH, url_params=url_params, with_token=True, with_proxy=False)
            if total != response['total']:
                total = response['total']
            businesses = response['businesses']
            for business in businesses:
                if business_in_US(business):
                    connector.enter_business_record(sanitize_business_object(business))
                    checked = checked + 1

            i = i + 1
            if len(response['businesses']) < 50 or i == 20:
                break
    except Exception:
        logger.error("Error faced while fetching business of area.")
        logger.exception("Exception: ")
        print("Error while parsing zip code")
    logger.info("Total :" + str(total) + " Counted: " + str(checked))
    print("Total :" + str(total) + " Counted: " + str(checked))
    connector.update_zip_code_counts(zip, total, checked)

def update_primary_city():
    zip_tuple = connector.get_all_business_zip()
    cities_tuple = connector.get_primary_city_for_zip()
    zips = [z[0] for z in zip_tuple]
    print(zips)
    cities = [(format(z[0], '05d'), z[1]) for z in cities_tuple]
    for c in cities:
        if c[0] == '89917':
            print("hi")
    cities = list(filter(lambda x: x[0] in zips, cities))
    print(len(cities))
    connector.update_primary_city(cities)

if __name__ == '__main__':
    update_primary_city()
