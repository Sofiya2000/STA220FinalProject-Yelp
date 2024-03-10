import requests
from bs4 import BeautifulSoup
import csv

def scrape_and_save_data(url, csv_file):
    """
    Scrapes data from a webpage containing a table and saves it to a CSV file.

    Args:
    - url (str): The URL of the webpage with the table.
    - csv_file (str): The path to the CSV file to save the data.

    Returns:
    - None
    """
    # Send an HTTP request to the webpage
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Determine the data type based on the URL
    if "individual_income_table" in url:
        table_id = "individual_income_table"
    elif "household_income_table" in url:
        table_id = "household_income_table"
    else:
        print("Table ID not found in URL.")
        return

    # Extract the table
    table = soup.find("table", {"id": table_id})

    if table is None:
        print(f"Table with ID '{table_id}' not found.")
        return

    # Extract table headers
    headers = [header.text.strip() for header in table.find_all("th")]

    # Remove the "Data Points" header
    headers.remove("Data Points")

    # Create a CSV file to write the data
    with open(csv_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)  # Write the headers to the CSV file

        # Extract table rows
        rows = table.find_all("tr")
        for row in rows[1:]:  # Exclude the header row
            # Extract data from each cell in the row except the last one (Data Points)
            data = [cell.text.strip() for cell in row.find_all("td")[:-1]]
            writer.writerow(data)  # Write the row data to the CSV file


if __name__ == "__main__":
    scrape_and_save_data("https://dqydj.com/scripts/cps/2021_income_calculators/2021_individual_income_table.html", "../data/individual_income_data.csv")
    scrape_and_save_data("https://dqydj.com/scripts/cps/2021_income_calculators/2021_household_income_table.html", "../data/household_income_data.csv")
