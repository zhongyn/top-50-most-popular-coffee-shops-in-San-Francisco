"""
Yelp API v2.0 code.

This program uses the Search API to query for 1000 coffee shops in San Francisco.
The center of the search area is Civic Center Plaza and the radius is 8000 meters.
The attributes extracted include name, review_count, and rating. They are written to 
the file "yelp_data.json".

"""
import json
import pprint
import sys
import urllib
import urllib2

import oauth2


API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'coffee'
DEFAULT_LOCATION = 'San Francisco, CA'
CATEGORY_FILTER = 'coffee'
RADIUS_FILTER = 8000
MAX_BUSINESSES = 1000
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = 'mDfgLw7Dtk4swa0BDzxreQ'
CONSUMER_SECRET = '92XPwVjLzsscJq-6uZ9HChV3JmE'
TOKEN = 'Gzv86IM2Q3A-AzULq1eHdWftJxn8eQZ7'
TOKEN_SECRET = 'HBq3xK0pAbmqvC_RZrCx-zfa9DE'


def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'http://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()
    
    print u'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response

def search(term, location, offset):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """
    
    url_params = {
        # 'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'offset': offset,
        'category_filter': CATEGORY_FILTER,
        'radius_filter': RADIUS_FILTER
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)


def query_api(term, location):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    name = []
    address = []
    review_count = []
    rating = []
    data = open('yelp_data.json', 'w+')

    for offset in xrange(0,MAX_BUSINESSES,20):
        response = search(term, location, offset)
        print response
        businesses = response.get('businesses')
        print u'offset: {0}'.format(offset)
        for b in businesses:
            name.append(b.get('name'))
            address.append(b.get('location').get('display_address'))
            review_count.append(b.get('review_count'))
            rating.append(b.get('rating'))
    yelp_data = {'name': name, 'review_count': review_count, 'rating': rating, 'address': address}

    data.write(json.dumps(yelp_data))


def main():
    try:
        query_api(DEFAULT_TERM, DEFAULT_LOCATION)
    except urllib2.HTTPError as error:
        sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))


if __name__ == '__main__':
    main()
