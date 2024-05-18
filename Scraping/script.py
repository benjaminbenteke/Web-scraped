import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
from urllib.parse import urlparse, parse_qs
import re
from datetime import datetime


def get_date(url):
    # Regular expression pattern to match the date in the URL
    pattern = r'/(\d{4}-\d{4})/week-\d+-ending-(\w+-\d+)-(\d{4})\.html'

    # Extracting the date from the URL using regular expressions
    match = re.search(pattern, url)
    # Map month names to their corresponding numbers
    month_map = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12
     }

    if match:
        year_range = match.group(1)
        week_ending = match.group(2)
        year = match.group(3)
        month_name, day = week_ending.split("-")

        # Get the month number from the map
        month_number = month_map[month_name.lower()]
        if len(str(day))==1:
            day= str(0)+str(day)

        # Format the date
        formatted_date = f"{year}-{month_number:02d}-{day}"
        return formatted_date

#############
url= "https://www.canada.ca/en/public-health/services/surveillance/respiratory-virus-detections-canada.html"
#############

links= ["https://www.canada.ca/en/public-health/services/surveillance/respiratory-virus-detections-canada/2013-2014.html",
        "https://www.canada.ca/en/public-health/services/surveillance/respiratory-virus-detections-canada/2014-2015.html",
        "https://www.canada.ca/en/public-health/services/surveillance/respiratory-virus-detections-canada/2015-2016.html",
        "https://www.canada.ca/en/public-health/services/surveillance/respiratory-virus-detections-canada/2016-2017.html",
        "https://www.canada.ca/en/public-health/services/surveillance/respiratory-virus-detections-canada/2017-2018.html",
        "https://www.canada.ca/en/public-health/services/surveillance/respiratory-virus-detections-canada/2018-2019.html",
        "https://www.canada.ca/en/public-health/services/surveillance/respiratory-virus-detections-canada/2019-2020.html",
        "https://www.canada.ca/en/public-health/services/surveillance/respiratory-virus-detections-canada/2020-2021.html",
        "https://www.canada.ca/en/public-health/services/surveillance/respiratory-virus-detections-canada/2021-2022.html",
        "https://www.canada.ca/en/public-health/services/surveillance/respiratory-virus-detections-canada/2022-2023.html",
        "https://www.canada.ca/en/public-health/services/surveillance/respiratory-virus-detections-canada.html"
          
          ]


dictt= {
    "2013-2014":["mwsbodytext text parbase section", "table table-bordered table-hover table-condensed"],
    "2014-2015":["mwsbodytext text parbase section", "table table-bordered table-hover table-condensed"],
    "2015-2016":["mwsbodytext text parbase section", "table table-bordered table-hover table-condensed"],
    "2016-2017":["mwsbodytext text parbase section", "table table-bordered table-hover table-condensed"],
    "2017-2018":["mwsbodytext text parbase section", "table table-bordered table-hover table-condensed"],
    "2018-2019":["mwsbodytext text parbase section", "table table-bordered table-hover table-condensed"],
    "2019-2020":["mwsbodytext text parbase section", "table table-bordered table-hover table-condensed"],
    "2020-2021":["mwsbodytext text parbase section", "table table-bordered table-hover table-condensed"],
    "2021-2022":["mwsbodytext text parbase section", "table table-bordered table-hover table-condensed"],
    "2022-2023":["mwsbodytext text parbase section", "table table-bordered table-hover table-condensed"],
    "2023-2024":["mwsgeneric-base-html parbase section", "table table-bordered table-hover table-condensed small text-center mrgn-lft-0"],
    
}


url= links[-1]

year= None

if any(char.isdigit() for char in url):
    match = re.search(r'/(\d{4})-(\d{4})\.html', url)

    if match:
        start_year, end_year = match.groups()
        year = f"{start_year}-{end_year}"
else:
    year= "2023-2024"
    
class_=dictt[year][0]
table= dictt[year][1]

page= requests.get(url)
soup= BeautifulSoup(page.content, "html.parser")

div_with_urls = soup.find('div', class_=class_)

weeks= []

if div_with_urls:
    # Find all anchor tags within the div
    anchor_tags = div_with_urls.find_all('a')

    # Print the href attribute (URL) of each anchor tag
    for anchor in anchor_tags:
        href = anchor.get('href')
        if href:
            weeks.append((href.rsplit('/')[-1]).rsplit('-ending')[0])
            print(href)
else:
    print("Div with the specified class not found.")

index_week= 2
wk= weeks[index_week:][0]

urls= []
if div_with_urls:
    # Find all anchor tags within the div
    anchor_tags = div_with_urls.find_all('a')

    # Extract and follow each URL
    for anchor in anchor_tags:
        href = anchor.get('href')
        if href:
            full_url = urljoin(url, href)  # Handle relative URLs
            print(f"Following URL: {full_url}")
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
    

urls= [urls[index_week]] # To select the recent date.

def extract_table_data(url, csv_writer,table):
    url_path = urlparse(url).path

    # Split the path and get the part containing the week number
    week_part = url_path.split('/')[-1]

    # Extract the week number
    week_number = week_part.split('-')[1]
    
    # table table-bordered table-hover table-condensed
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table by its attributes (you might need to inspect the HTML to get the right selector)
    table = soup.find('table', class_=table)  # Replace with the actual class or use other methods
#     table = soup.find('table', class_=tables[0])  # Replace with the actual class or use other methods

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



# Create a CSV file for all URLs
# year= "2023 - 2024 Season"
csv_filename = 'output'+year+'.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Loop through URLs and extract data to the CSV file
    for url in urls:
        extract_table_data(url, csv_writer,table)

print(f"All table data saved to {csv_filename}")

data= pd.read_csv(csv_filename)

data.drop(data[data['Reporting Laboratory'] == 'Reporting Laboratory'].index, inplace=True)

data = data.sort_values(by='Reporting Laboratory', ascending=True)

## 
new_column_name = 'week'
data = data.rename(columns={data.columns[0]: new_column_name})
data["week"]= data["week"].apply(lambda x: x[4:])



data = data.rename(columns={'Flu Tested': 'Flu Test'})
data = data.rename(columns={'SARS-CoV-2 Tested': 'SARS-CoV-2 Test'})
data = data.rename(columns={'RSV Tested': 'RSV Test'})
data = data.rename(columns={'HPIV Tested': 'HPIV Test'})
data = data.rename(columns={'ADV Tested': 'ADV Test'})
data = data.rename(columns={'HMPV Tested': 'HMPV Test'})
data = data.rename(columns={'EV/RV Tested': 'EV/RV Test'})
data = data.rename(columns={'HCoV Tested': 'HCoV Test'})

columns = data.columns.tolist()

# Specify the column to move
column_to_move = 'week'

# Specify the target position (0-based index)
target_position = 1

# Remove the column from its current position
columns.remove(column_to_move)

# Insert the column at the target position
columns.insert(target_position, column_to_move)

# Create a new DataFrame with columns in the desired order
df_reordered = data[columns]

df_reordered[df_reordered["Reporting Laboratory"]== "CANADA"]

df_reordered["Reporting Laboratory"].value_counts()

dt = df_reordered.reset_index(drop=True)

dt.sort_values(by='week', ascending=False)
#dt = dt[dt['Week'] == wk]
dt= dt.rename(columns={'Reporting Laboratory': 'province'})
d_new= [get_date(urls[0]) for _ in range(len(dt))]
dt.insert(6, 'date', d_new)

dt.to_csv("Scraping/data_"+str(wk)+'.csv', index= False)

past_data= pd.read_csv("Scraping/RVDSS_all_Canada.csv")

# dt.to_csv("data_"+str(wk)+'.csv', index= False)


# past_data= pd.read_csv("RVDSS_all_Canada.csv")
Province_list= list(past_data[['province']].value_counts().keys())
Province_list= [f[0] for f in Province_list]
Province_list.sort()

def convert(dic):
    for key in dic.keys():
        v= dic[key]
#         print(dic[key])
        dic[key]= [v]
    return dic

def custom_merge(df1, df2):
    # df1: former dataset
    # df2: new dataset
    d= None
    s= "2023-2024"
    for prov in Province_list:
        if len(df2.loc[df2['province']==prov].to_dict(orient='records'))!=0:
            d= df2.loc[df2['province']==prov].to_dict(orient='records')[0]
            d['date']= s
            d['season']= s
            d['phufull']= prov
            d['year']= s[5:]
            d= pd.DataFrame(convert(d))
            df1= pd.concat([df1, d], ignore_index=True)#df1.append(d, ignore_index=True)
        

    df1 = df1.sort_values(by='province', ascending=True)
    return df1

dtt= custom_merge(past_data, dt)

duplicates_mask = dtt.duplicated()

# Then filter the DataFrame based on this mask
duplicated_rows = dtt[duplicates_mask]


# dtt.to_csv("RVDSS_all_Canada"+".csv", index= False)
dtt.to_csv("Scraping/"+"RVDSS_all_Canada"+".csv" , index= False)

## END

## END
