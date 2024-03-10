import os
import pandas as pd
import requests
from ExtractCityName import extract_metro_names

def remove_empty_price_entries(csv_filename):
    """
    Remove rows with empty "price" values from the CSV file.

    Args:
    - csv_filename (str): The filename of the CSV file.

    Returns:
    - None
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_filename)

    # Remove rows with empty "price" values
    df = df.dropna(subset=['price'])

    # Save the modified DataFrame back to the CSV file
    df.to_csv(csv_filename, index=False)

    print('Removed rows with empty "price" values from the CSV file.')

def searchLookUp(term, categories, location, output_filename):
    """
    Searches for businesses based on the provided term, categories, and location using the Yelp API.

    Args:
    - term (str): The search term.
    - categories (str): The categories to search for.
    - location (str): The location to search in.
    - output_filename (str): The filename to save the search results.

    Returns:
    - None
    """
    # Clean location name for directory creation
    cleaned_location = location.replace(', ', '_').replace(' ', '_').replace('/', '_')

    # Output directory construction
    output_dir = '../data/'
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

    # Output filename construction
    output_filename = '{}{}_{}.csv'.format(output_dir, term, cleaned_location)

    # Initialization of variables
    offset, limit, total, entries = 0, 50, 20, []

    # Searching Yelp for businesses
    print('Looking into Yelp for {} in {}'.format(term, location))
    while offset < min(10, total):  # Limit to 10 pages or total businesses
        print("Page #{}".format(offset // limit + 1))

        # Yelp API request parameters
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

        # Sending request to Yelp API
        response = requests.get('{}{}'.format(yelp_api_path, search_api_path), params=params, headers=headers)
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(response.text)

        # Processing JSON response
        json_output = response.json()
        total = json_output['total']
        entries += json_output['businesses']
        offset += limit

    # Saving results to CSV file
    if entries:
        df = pd.DataFrame(entries)
        try:
            if 'price' in df.columns and not df['price'].isnull().all():
                df = df[fields]  # Select only required fields
                df.to_csv(output_filename, index=False)
                print('-----------------------')
                print('Total of {} entries saved to {}'.format(len(entries), output_filename))
                remove_empty_price_entries(output_filename)
            else:
                print('No entries with valid "price" found for {} in {}. Skipping saving to CSV.'.format(term, location))
        except KeyError as e:
            print("Error: Field '{}' not found in retrieved data. Skipping saving to CSV.".format(e))
    else:
        print('No entries found for {} in {}'.format(term, location))

if __name__ == "__main__":
    # Example usage
    # search_locations = extract_metro_names("../data/individual_income_data.csv")
    search_locations = extract_metro_names("../data/household_income_data.csv")
    search_categories, search_term = "restaurants", "Mexican"
    yelp_api_key = 'QeGMmbsLY4LHkg-ZDkcJKFzrzaPPfKwIeCu_L0m_rvSAfA9OFM6E1nd2cjxUyYY6gExP8nYSvg4rAANbedzUbDk8oM2M-tNIkFiCoSfFj0YH7Yhf-6Nv71hoouvsZXYx'
    yelp_api_path, search_api_path = 'https://api.yelp.com', '/v3/businesses/search'
    fields = ['id','name','price','rating','review_count','url']

    # Perform Yelp searches for each location
    for location in search_locations:
        output_filename = '{}_{}.csv'.format(search_term, location.replace(', ', '_').replace(' ', '_'))
        searchLookUp(search_term, search_categories, location, output_filename)
