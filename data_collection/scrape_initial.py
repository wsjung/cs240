from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# constants
SCROLL_PAUSE_TIME = 0.5

# list of stocks
stocks = ['BTC','BCH','ETH','EOS','XRP']
stocks = [s + '-USD' for s in stocks]

print (stocks)

url = 'https://finance.yahoo.com/quote/ETH-USD/history?p=ETH-USD'
browser = webdriver.Chrome()
browser.get(url)

time.sleep(2)
print ("wake")

### Filter Max duration and apply
# click date interval selection
browser.find_elements_by_xpath("//span[contains(@class, 'C($c-fuji-blue-1-b)') and contains(@class, 'Mstart(8px)') and contains(@class, 'Cur(p)')]")[0].click()
print ("clicked!")
# select max interval
browser.find_elements_by_xpath("//span[contains(@class, 'P(5px)') and contains(@class, 'W(37px)')]")[7].click()
print ("clicked MAX")
time.sleep(3)
# select Done
browser.find_element_by_xpath("//button[contains(@class, 'Miw(80px)!') and contains(@class, 'Fl(start)')]").click()
print ("clicked Done")
# select Apply
browser.find_element_by_xpath("//button[contains(@class, 'Py(9px)') and contains(@class, 'Fl(end)')]").click()
print ("clicked Apply")
time.sleep(2)

# count number of page down scrolls
countScroll = 0;

length_page = browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight); var lenPage=document.documentElement.scrollHeight; return lenPage;")
print("scroll!")

while True:
	last_length = length_page
	time.sleep(SCROLL_PAUSE_TIME)
	length_page = browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight); var lenPage=document.documentElement.scrollHeight; return lenPage;")
	countScroll = countScroll + 1
	if last_length==length_page:
		break
	print("scroll!")
print("Total scrolls to bottom of page: %d" % countScroll)

response = browser.page_source
browser.quit()
print ("browser quit")

# parse wih BeautifulSoup
soup = BeautifulSoup(response, features="html.parser")

# for each data row, strip all but the text
for row in soup.find_all('tr', {'class' : 'BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)'}):
	#print (row.contents)
	for col in row.contents:
		print (col.string)