import json
import numpy as np

YELP_DATA_PATH = 'yelp_data.json'
WEIGHT_REVIEW_COUNT = 0.5
WEIGHT_RATING = 0.5

def read_data():
    with open(YELP_DATA_PATH) as yelp_data:
        data = json.load(yelp_data)
    return data

def popularity(data):
    """Compute the popularities of coffee shops and sort them descendingly.

    Args:
        data (dict): coffee shop info (name, address, rating, review_count)
    """
    num_of_businesses = len(data['name'])

    pop = np.zeros(num_of_businesses, dtype=[('id', 'i4'), ('popularity', 'f4')])
    pop['id'] = np.arange(num_of_businesses)

    review_count = np.array(data['review_count'], dtype='f4')
    rating = np.array(data['rating'], dtype='f4')

    pop['popularity'] = review_count / np.amax(review_count) * WEIGHT_REVIEW_COUNT + rating / np.amax(rating) * WEIGHT_RATING
    sorted_pop = np.sort(pop, order=['popularity'])[::-1]    


    name = data['name']
    address = data['address']
    sorted_name = []
    sorted_address = []
    rank = open('top_50_most_popular_coffee_shops.csv', 'w+')

    for i in sorted_pop['id']:
        sorted_name.append(name[i])
        sorted_address.append(address[i])

    result = zip(sorted_name, sorted_pop['popularity'], sorted_address)
    rank.write('\n'.join('{}, {}, {}'.format(x[0].encode('utf8'),x[1],', '.join([y.encode('utf8') for y in x[2]])) for x in result))

def main():
    popularity(read_data())


if __name__ == '__main__':
    main()