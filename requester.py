import requests
import yaml
import random
from logger import logger

# from logger import logger

# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    from urllib.parse import quote
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib import quote

# https://www.yelp.com/developers/v3/manage_app
with open("conf.yaml", 'r') as stream:
    content = yaml.safe_load(stream)
    ACCESS_TOKEN = content.get('access_token')
    ZYTE_API_KEY = content.get('zyte_api_key')


def generic_request(host, path, url_params=None, with_token=False):
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
    headers = {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    if with_token:
        headers['Authorization'] = 'Bearer %s' % get_random_api_key()

    logger.info(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params,
                                proxies={
                                    "http": "http://" + ZYTE_API_KEY + ":@proxy.crawlera.com:8011/",
                                    "https": "http://" + ZYTE_API_KEY + ":@proxy.crawlera.com:8011/",
                                },
                                verify='./zyte-proxy-ca.crt'
                                )

    if response.status_code != 200:
        logger.error("request failed for url: " + url)
        print("request failed for url: " + url)

    return response


def request_json(host, path, url_params=None, with_token=False):
    return generic_request(host, path, url_params, with_token).json()


def get_random_api_key():
    return ACCESS_TOKEN[random.randint(0, len(ACCESS_TOKEN) - 1)]['api_key']
