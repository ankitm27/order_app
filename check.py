import csv, sqlite3
with open('Scrape_Test.csv','rb') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin)
    to_do = []# comma is default delimiter
    to_db = [(i['Product Name']) for i in dr]
    print to_do
