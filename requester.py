import requests
import yaml
import random

from logger import logger

# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode

# https://www.yelp.com/developers/v3/manage_app
with open("conf.yaml", 'r') as stream:
    ACCESS_TOKEN = yaml.safe_load(stream).get('access_token')


def request(host, path, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % get_random_api_key(),
    }

    logger.info(u'Querying {0} ...'.format(url_params))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()

def get_random_api_key():
    return ACCESS_TOKEN[random.randint(0,len(ACCESS_TOKEN)-1)]['api_key']