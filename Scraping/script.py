import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
from urllib.parse import urlparse, parse_qs
import re

def scrape(url):
    page= requests.get(url)
    soup= BeautifulSoup(page.content, "html.parser")
#     div_with_urls = soup.find('div', class_='mwsgeneric-base-html parbase section')
    div_with_urls = soup.find('div', class_='mwsbodytext text parbase section')

    if div_with_urls:
        anchor_tags = div_with_urls.find_all('a')
        for anchor in anchor_tags:
            href = anchor.get('href')
#             if href:
#                 print(href)
#     else:
#         print("Div with the specified class not found.")
   
    urls= []
    if div_with_urls:
        anchor_tags = div_with_urls.find_all('a')

        for anchor in anchor_tags:
            href = anchor.get('href')
            if href:
                full_url = urljoin(url, href)  # Handle relative URLs
                urls.append(full_url)

                # Make an HTTP request to the URL
                try:
                    response = requests.get(full_url)
                    # Process the response as needed
                    print(f"Response status code: {response.status_code}")
                except requests.RequestException as e:
                    print(f"Error making request: {e}")

    else:
        print("Div with the specified class not found.")
    
    return urls


def extract_table_data(url, csv_writer):
    url_path = urlparse(url).path

    # Split the path and get the part containing the week number
    week_part = url_path.split('/')[-1]

    # Extract the week number
    week_number = week_part.split('-')[1]
    
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table by its attributes (you might need to inspect the HTML to get the right selector)
    table = soup.find('table', class_='table table-bordered table-hover table-condensed small text-center mrgn-lft-0')  # Replace with the actual class or use other methods

    if table:
        # Extract data from the table
        rows = table.find_all('tr')  # Find all rows in the table
        

        # Loop through rows
        for row in rows:
            # Extract and write the text content of each cell in the current row
            row_data = []
            row_data.insert(1, f"Week {week_number}")
            cells = row.find_all(['th', 'td'])
            for cell in cells:
                row_data.append(cell.text.strip())
        
            
            # Write the row data to the CSV file
            csv_writer.writerow(row_data)
    else:
        print(f"Table with the specified class not found on {url}")
        

# # Create a CSV file for all URLs
# match = re.search(r'/(\d{4})-(\d{4})\.html', url)

# if match:
#     start_year, end_year = match.groups()
#     year = f"{start_year}-{end_year}"
    
# # year= "2023 - 2024 Season"
# csv_filename = 'output'+year+'.csv'+"Season"
# with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
#     csv_writer = csv.writer(csvfile)

#     # Loop through URLs and extract data to the CSV file
#     for url in urls:
#         extract_table_data(url, csv_writer)

# print(f"All table data saved to {csv_filename}")






def cleaning(url):

    match = re.search(r'/(\d{4})-(\d{4})\.html', url)

    if match:
        start_year, end_year = match.groups()
        year = f"{start_year}-{end_year}"
    else:
        year= "2022-2023"
        
    
    csv_filename = 'output'+year+'.csv'+"Season"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
         csv_writer = csv.writer(csvfile)

         # Loop through URLs and extract data to the CSV file
         for url in urls:
                extract_table_data(url, csv_writer)
        
        
    data= pd.read_csv(csv_filename)  
    data.drop(data[data['Reporting Laboratory'] == 'Reporting Laboratory'].index, inplace=True)
    data = data.sort_values(by='Reporting Laboratory', ascending=True)
    new_column_name = 'Week'
    data = data.rename(columns={data.columns[0]: new_column_name})
    data["Week"]= data["Week"].apply(lambda x: x[4:])
    
    columns = data.columns.tolist()

    # Specify the column to move
    column_to_move = 'Week'

    # Specify the target position (0-based index)
    target_position = 1

    # Remove the column from its current position
    columns.remove(column_to_move)

    # Insert the column at the target position
    columns.insert(target_position, column_to_move)

    # Create a new DataFrame with columns in the desired order
    df_reordered = data[columns]
    
    return df_reordered