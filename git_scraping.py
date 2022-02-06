# I think the D.C. Police department’s “crime cards” website is a great candidate for automated scraping.
# The site contains a table with details about all crimes over the past two years city-wide, based on DC criminal code offense definitions (so, they might reflect crimes not reported to the FBI’s UCR program).
# Since the data stretches back for two years, keeping an automated scraper running could help build a time-series profile of crime in D.C.
# We could write stories about the patterns and trends in the city’s crime rates, what crimes are being committed, where crimes are occurring (down to the block, because it includes that data); there are lots of possibilities.
# We might even be able to combine the data with prosecution data to look at the incident to arrest to sentencing pipeline for particular crimes.

# importing necessary packages
import csv
import requests
from bs4 import BeautifulSoup

# saving the site url
url = 'https://dcatlas.dcgis.dc.gov/crimecards/'
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
html = response.content
# This is throwing an error: says {requests.exceptions.SSLError: HTTPSConnectionPool(host='dcatlas.dcgis.dc.gov', port=443): Max retries exceeded with url: /crimecards (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1129)')))} Tried troubleshooting but got a little lost Maybe we can talk about it in class.
soup = BeautifulSoup(html, features="html.parser")

table = soup.find(#html tag for the table is "<tbody _ngcontent-rkj-c35 data-read-aloud multi-block=“true”>", not sure whether I can jsut put that in)
list_of_rows = [] # permanent list
for row in table.find_all('tr'): #each row within the table is contained in a 'tr' tag)
    list_of_cells = [] # temp list (gets appended to permanent list and then overwritten)
    for cell in row.find_all('td'):# each "cell" of info within each row is contained in a td tag
        if cell.find('legend'):
            pass # skip the legend tag (probably a more complex command than 'pass,'but I don't want what's contained in the legend element)
        else:
        text = cell.text.strip()
        # Here I'd tell it to separate text by the <br> tag if I could; I want to make sure scraped info is separated properly for a csv format.
        list_of_cells.append(text)
    list_of_rows.append(list_of_cells)

print(list_of_rows)
outfile = open("./dc-crime.csv", "w")
writer = csv.writer(outfile)
writer.writerow(["offense", "block","anc", "ward", "psa", "district", "report_date_time", "offense_date_time"])
writer.writerows(list_of_rows)
