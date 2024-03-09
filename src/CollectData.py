import pandas as pd
import requests

search_locations = ["New York City, NY", "Queens, NY", 'Los Angeles, CA', 'San Francisco, CA', 'Chicago, IL', 'Houston, TX', 'Philadelphia, PA', 'Phoenix, AZ', 'San Antonio, TX', 'San Diego, CA', 'Dallas, TX', 'San Jose, CA', 'Austin, TX', 'Jacksonville, FL', 'Indianapolis, IN', 'Columbus, OH', 'Fort Worth, TX', 'Charlotte, NC', 'Seattle, WA', 'Denver, CO', 'El Paso, TX', 'Detroit, MI', 'Washington, DC', 'Boston, MA', 'Memphis, TN', 'Nashville, TN', 'Portland, OR', 'Oklahoma City, OK', 'Las Vegas, NV', 'Baltimore, MD', 'Louisville, KY', 'Milwaukee, WI', 'Albuquerque, NM', 'Tucson, AZ', 'Fresno, CA', 'Sacramento, CA', 'Kansas City, MO', 'Long Beach, CA', 'Mesa, AZ', 'Atlanta, GA', 'Colorado Springs, CO', 'Virginia Beach, VA', 'Raleigh, NC', 'Omaha, NE', 'Miami, FL', 'Oakland, CA', 'Minneapolis, MN', 'Tulsa, OK', 'Wichita, KS', 'New Orleans, LA', 'Arlington, TX']
search_categories, search_term = "restaurants", "Australian"
yelp_api_key = 'add_your_yelp_api_key_here'
yelp_api_path, search_api_path = 'https://api.yelp.com', '/v3/businesses/search'
fields = ['id','name','price','rating','review_count','url']

def search(term, categories, location):
    output_filename = '{}_{}.csv'.format(term, location.replace(', ', '_').replace(' ', '_'))
    offset, limit, total, entries = 0, 50, 20, []
    print('Looking into Yelp for {} in {}'.format(term, location))
    while offset < min(10, total):
        print("Page #{}".format(offset // limit + 1))
        params = {
            "term": term,
            "categories": categories,
            "location": location,
            "radius": 6000,
            "locale": "en_US",
            "limit": min(total - offset, limit),
            "offset": offset,
        }
        headers = {
            "Authorization": "Bearer {}".format(yelp_api_key),
        }
        response = requests.get('{}{}'.format(yelp_api_path, search_api_path), params=params, headers=headers)
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(response.text)
        json_output = response.json()
        total = json_output['total']
        entries += json_output['businesses']
        offset += limit

    if entries:
        df = pd.DataFrame(entries)
        try:
            df = df[fields]  # Select only required fields
            df.to_csv(output_filename, index=False)
            print('-----------------------')
            print('Total of {} entries saved to {}'.format(len(entries), output_filename))
        except KeyError as e:
            print("Error: Field '{}' not found in retrieved data. Skipping saving to CSV.".format(e))
    else:
        print('No entries found for {} in {}'.format(term, location))

if __name__ == "__main__":
    for location in search_locations:
        search(search_term, search_categories, location)
