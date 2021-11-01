from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd

s = HTMLSession()
proDesc = []
# phone = 'Search'
url = 'https://web.whatsapp.com/'

def getdata(url):
	r = s.get(url)
	r.html.render(sleep=3)
	soup = BeautifulSoup(r.html.html, 'html.parser')
	return soup



def parse(soup):
	obj = soup.find_all("div",{'data-pre-plain-text':''})

	for item in obj:
		# title =  item.find("a",{'class':"a-link-normal a-text-normal"}).text.strip()
		try:
			msg =  item.find("span",{'class':"i0jNr selectable-text copyable-text"}).text.strip()
			# rating = item.find("span",{'class':"a-icon-alt"}).text.strip()
		except:
			msg = 0
			# rating = 0

		products = {
			# 'title':title,
			'msg':msg,
			# 'rating':rating
		}	
		proDesc.append(products)
	return	


soup = getdata(url)
parse(soup)

df = pd.DataFrame(proDesc)

df.to_csv('message.csv',index=False)
print(df.head())
print("THE END")