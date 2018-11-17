from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sqlite3

# constants
SCROLL_PAUSE_TIME = 0.5

# list of stocks
stocks = ['BTC','BCH','ETH','EOS','XRP']
stocksUSD = [s + '-USD' for s in stocks]

print (stocks)

# constants
url = 'https://finance.yahoo.com/quote/ETH-USD/history?p=ETH-USD'
sqlite_file = './stocks.db'

# sqlite db connection
connection = sqlite3.connect(sqlite_file)
cursor = connection.cursor()

# webdriver
browser = webdriver.Chrome()

def scrape(browser, cursor, stock):

	stockUSD = stock + "-USD"

	url = ('https://finance.yahoo.com/quote/%s/history?p=%s' % (stockUSD,stockUSD))
	browser.get(url)
	# SQLite relations
	table_name = stock

	time.sleep(2)
	print('loading', end='', flush=True)
	### Filter Max duration and apply
	# click date interval selection
	browser.find_elements_by_xpath("//span[contains(@class, 'C($c-fuji-blue-1-b)') and contains(@class, 'Mstart(8px)') and contains(@class, 'Cur(p)')]")[0].click()
	print('.', end='', flush=True)
	time.sleep(0.5)
	# select max interval
	browser.find_elements_by_xpath("//span[contains(@class, 'P(5px)') and contains(@class, 'W(37px)')]")[7].click()
	print('.', end='', flush=True)
	time.sleep(0.5)
	# select Done
	browser.find_element_by_xpath("//button[contains(@class, 'Miw(80px)!') and contains(@class, 'Fl(start)')]").click()
	print('.', end='', flush=True)
	time.sleep(0.5)
	# select Apply
	browser.find_element_by_xpath("//button[contains(@class, 'Py(9px)') and contains(@class, 'Fl(end)')]").click()
	print('.', flush=True)
	time.sleep(1)
	print('loaded')

	# count number of page down scrolls
	countScroll = 0;

	length_page = browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight); var lenPage=document.documentElement.scrollHeight; return lenPage;")
	print("scrolling", end='', flush=True)

	while True:
		last_length = length_page
		time.sleep(SCROLL_PAUSE_TIME)
		length_page = browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight); var lenPage=document.documentElement.scrollHeight; return lenPage;")
		countScroll = countScroll + 1
		print('.', end='', flush=True)
		if last_length==length_page:
			print('')
			break
	print("Total scrolls to bottom of page: %d" % countScroll)

	response = browser.page_source

	# parse wih BeautifulSoup
	soup = BeautifulSoup(response, features="html.parser")

	# for each data row, strip all but the text
	for row in soup.find_all('tr', {'class' : 'BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)'}):
		tup = "('"+row.contents[0].text+"'"
		for i in range(1,len(row)):
			c = row.contents[i].text
			if c=="-":
				c = 'null'
			tup = tup + "," + c.replace(',','')
		tup += ")"
		print("insert or ignore into %s values %s" % (stock,tup))
		cursor.execute("insert or ignore into %s values %s" % (stock,tup))

for stock in stocks:
	scrape(browser, cursor,stock)

# quit browser gracefully
browser.quit()
print ("browser quit")
# commit changes and close file
connection.commit()
connection.close