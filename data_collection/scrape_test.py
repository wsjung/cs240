# Unit-test for scrape_initial.py
# steps: 
### 1) install required package dependencies: 
##########`pip3 install -U -r requirements.txt`
### 2) run scrape_test.py
##########`python3 scrape_test.py`
#
#
# @author Woo Jung
# @version 1.0
from scrape_initial import scraper
import unittest

class TestScrapeFunctions(unittest.TestCase):

	# template URL
	URL= 'https://finance.yahoo.com/quote/%s/history?p=%s'
	# list of stocks
	stocks = ['BTC','BCH','ETH','EOS','XRP']

	URL_BTC='https://finance.yahoo.com/quote/BTC-USD/history?p=BTC-USD'
	URL_ETH='https://finance.yahoo.com/quote/ETH-USD/history?p=ETH-USD'
	URL_XRP='https://finance.yahoo.com/quote/XRP-USD/history?p=XRP-USD'

	# test stockURL() generations
	def test_stockURL_BTC(self):
		self.assertEqual(scraper.stockURL(self.URL,'BTC'), self.URL_BTC)

	def test_stockURL_ETH(self):
		self.assertEqual(scraper.stockURL(self.URL,'ETH'), self.URL_ETH)

	def test_stockURL_XRP(self):
		self.assertEqual(scraper.stockURL(self.URL,'XRP'), self.URL_XRP)

	# tests selenium browser automation
	def test_selenium(self):
		# init browser
		browser = scraper.startBrowser()
		# head to BTC page
		browser.get(self.URL_BTC)

		# should be this URL
		want_URL = 'https://finance.yahoo.com/quote/BTC-USD/history?period1=1279263600&period2=1542614400&interval=1d&filter=history&frequency=1d'

		# filter max interval
		scraper.filtering(browser)

		# assertion for URL equality
		self.assertEqual(browser.current_url, want_URL)

		# auto scroll to bottom of page
		scraper.scrollPage(browser, 0.5)

		# exit browser
		browser.quit()

	# test beautifulsoup html parsing
	### currently does not work
	### as there is no way to test dynamic source for a constantly updating webpage
	### => test functionality of beautifulsoup. 
	def test_bs(self):
		with open('./test_page.html', 'r') as f:
			res = f.read()
			soup = scraper.parsePage(res)
			self.assertEqual(scraper.parsePage(res),soup)

if __name__ == '__main__':
	unittest.main()