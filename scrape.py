# requests package fetches things from the web
import csv
import requests
from bs4 import BeautifulSoup

url = 'https://www.ola.state.md.us/Search/Report?keyword=&agencyId=&dateFrom=&dateTo='
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
html = response.content

soup = BeautifulSoup(html, features="html.parser")

table = soup.find('tbody')

list_of_rows = [] # permanent list
for row in table.find_all('tr'):
    list_of_cells = [] # temp list (gets appended to permanent list and then overwritten)
    for cell in row.find_all('td'):
        if cell.find('a'):
            list_of_cells.append("https://www.ola.state.md.us" + cell.find('a')['href']) # find the "a" tag, then find the href attribute within that tag
            # this gives us a relative url
        text = cell.text.strip()
        list_of_cells.append(text)
    list_of_rows.append(list_of_cells)

print(list_of_rows)
outfile = open("./reports.csv", "w")
writer = csv.writer(outfile)
writer.writerow(["date", "type", "url", "title"])
writer.writerows(list_of_rows)
