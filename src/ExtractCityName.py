import csv

def extract_metro_names(csv_file):
    """
    Extracts metro names from a CSV file containing individual income data.

    Args:
    - csv_file (str): The path to the CSV file.

    Returns:
    - list: A list of metro names.
    """
    search_locations = []

    # Open the CSV file
    with open(csv_file, "r") as csvfile:
        reader = csv.reader(csvfile)
        
        # Skip the header row
        next(reader)
        
        # Iterate over each row and extract the metro name from the first column
        for row in reader:
            metro_name = row[0]  # Assuming the metro name is in the first column
            search_locations.append(metro_name)

    return search_locations

if __name__ == "__main__":
    metro_names = extract_metro_names("individual_income_data.csv")
    for metro_name in metro_names:
        print(metro_name)

