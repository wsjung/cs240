from bs4 import BeautifulSoup
from requests import get

# list of stocks
stocks = ['BTC','BCH','ETH','EOS','XRP']
stocks = [s + '-USD' for s in stocks]

print (stocks)

url = 'https://finance.yahoo.com/quote/ETH-USD/history?p=ETH-USD'
response = get(url)

#print (response.text)

soup = BeautifulSoup(response.text, features="html.parser")

for row in soup.find_all('tr', {'class' : 'BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)'}):
	#print (row.contents)
	for col in row.contents:
		print (col.string)