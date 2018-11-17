from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sqlite3

# constants
SCROLL_PAUSE_TIME = 0.5
SQLITE_FILE ='./stocks.db'
URL= 'https://finance.yahoo.com/quote/%s/history?p=%s'

# list of stocks
stocks = ['BTC','BCH','ETH','EOS','XRP']
# stocksUSD = [s + '-USD' for s in stocks]

# sqlite db connection
connection = sqlite3.connect(SQLITE_FILE)
cursor = connection.cursor()

# webdriver
browser = webdriver.Chrome()

def stockURL(template, symb):
	symb += '-USD'
	return (template % (symb, symb))

def filtering(driver):
	time.sleep(2)
	print('loading', end='', flush=True)
	### Filter Max duration and apply
	# click date interval selection
	driver.find_elements_by_xpath("//span[contains(@class, 'C($c-fuji-blue-1-b)') and contains(@class, 'Mstart(8px)') and contains(@class, 'Cur(p)')]")[0].click()
	print('.', end='', flush=True)
	time.sleep(0.5)
	# select max interval
	driver.find_elements_by_xpath("//span[contains(@class, 'P(5px)') and contains(@class, 'W(37px)')]")[7].click()
	print('.', end='', flush=True)
	time.sleep(0.5)
	# select Done
	driver.find_element_by_xpath("//button[contains(@class, 'Miw(80px)!') and contains(@class, 'Fl(start)')]").click()
	print('.', end='', flush=True)
	time.sleep(0.5)
	# select Apply
	driver.find_element_by_xpath("//button[contains(@class, 'Py(9px)') and contains(@class, 'Fl(end)')]").click()
	print('.', end='', flush=True)
	time.sleep(1)
	print('loaded')

def scrollPage(driver, pause_time):
	# count number of page down scrolls
	countScroll = 0;

	length_page = driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight); var lenPage=document.documentElement.scrollHeight; return lenPage;")
	print("scrolling", end='', flush=True)

	while True:
		last_length = length_page
		time.sleep(pause_time)
		length_page = driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight); var lenPage=document.documentElement.scrollHeight; return lenPage;")
		countScroll = countScroll + 1
		print('.', end='', flush=True)
		if last_length==length_page:
			print('')
			break
	print("Total scrolls to bottom of page: %d" % countScroll)

	response = driver.page_source
	return response

def parsePage(page):
	return BeautifulSoup(page, features='html.parser')

def updateData(soup, cursor,rel_name):
	# for each data row, strip all but the text
	for row in soup.find_all('tr', {'class' : 'BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)'}):
		tup = "('"+row.contents[0].text+"'"
		for i in range(1,len(row)):
			c = row.contents[i].text
			if c=="-":
				c = 'null'
			tup = tup + "," + c.replace(',','')
		tup += ")"
		cursor.execute("insert or ignore into %s values %s" % (rel_name,tup))
		print ('>insert into %s' % rel_name)

# script run!!
for stock in stocks:
	print('initiating scrape for stock: %s' % stock)

	# browser points to stock URL
	surl = stockURL(URL,stock)
	browser.get(surl)
	print('browser launched')

	# SQLite table name
	table_name = stock

	# filter max interval
	filtering(browser)

	# scroll to bottom of page
	response = scrollPage(browser, SCROLL_PAUSE_TIME)

	# parse the response
	parsed = parsePage(response)

	# update the database
	updateData(parsed, cursor, stock)
	print('database update for %s completed' % stock)

# commit changes and close file
connection.commit()
print('database changes committed')
connection.close()
print('database connection closed')

# quit browser gracefully
browser.quit()
print('browser exit')