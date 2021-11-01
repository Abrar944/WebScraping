from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import argparse

#Comment out these 3 lines and change the searchterm variable, if you do not wish to use argparse version
my_parser = argparse.ArgumentParser(description='Return  Amazon Products')
my_parser.add_argument('searchterm', metavar='searchterm', type=str, help='The item to be searched for. Use + for spaces')
args = my_parser.parse_args()

searchterm = args.searchterm

s = HTMLSession()
dealslist = []


url = f'https://www.amazon.in/s?k={searchterm}'
#url = 'https://www.amazon.in/s?k=laptops'

def getdata(url):
    r = s.get(url)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup

    print(soup)

def getdeals(soup):
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    for item in products:
        title = item.find('a', {'class': 'a-link-normal a-text-normal'}).text.strip()
        # short_title = item.find('a', {'class': 'a-link-normal a-text-normal'}).text.strip()[:25]
        link = item.find('a', {'class': 'a-link-normal a-text-normal'})['href']
        try:
            saleprice = item.find('span', {'class': 'a-price-whole'}).text.strip()
            #oldprice = item.find_all('span', {'class': 'a-offscreen'}).text.strip()
            reviews = item.find('span', {'class': 'a-icon-alt'}).text.strip() 
        except:
            #oldprice = item.find('span', {'class': 'a-letter-space'}).text.strip()
            saleprice = 0
            reviews = 0
        saleitem = {
            'title': title,
            'link': link,
            'saleprice': saleprice,
            'reviews': reviews            
            }
        dealslist.append(saleitem)
    return 

def getnextpage(soup): 
    pages = soup.find('ul', {'class': 'a-pagination'})   
    if not pages.find('li', {'class': 'a-disabled a-last'}):
        url = 'https://www.amazon.in/s?k' + str(pages.find('li', {'class': 'a-last'}).find('a')['href'])
        return url
    else:
        return

while True:
    soup = getdata(url)
    getdeals(soup)
    url = getnextpage(soup)
    if not url:
        break
    else:
        print(url)
        print(len(dealslist))  


df = pd.DataFrame(dealslist)
df.to_csv(searchterm + '-deals.csv', index=False)
print('Finished.')

