# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.ui import Select
import locale
import dateutil.parser as parser
locale.setlocale(locale.LC_TIME, 'fr_FR.utf-8')


driver = webdriver.Chrome('/home/igor/Downloads/chromedriver_linux64/chromedriver')

driver.get('https://teleservices.paris.fr/srtm/deconnexionAccueil.action')

def to_datetime(s):
	d = parser.parse(s, dayfirst=True)
	return d


class Spot :
	def __init__(self, date, hour, club, court_number) :
		self.date = date
		self.hour = hour
		self.club = club
		self.court_no = court_number


class Session :

	def __init__(self, driver, login, password, spots) :
		self.driver = driver
		self.login = login
		self.password = password
		self.spots = spots


	def authenticate(self) :
		self.driver.get('https://teleservices.paris.fr/srtm/deconnexionAccueil.action')
		login_input = self.driver.find_element_by_name('login')
		passwd_input = self.driver.find_element_by_name('password')
		login_input.clear()
		login_input.send_keys(self.login)
		passwd_input.clear()
		passwd_input.send_keys(self.password)
		passwd_input.send_keys(Keys.RETURN)

	def search_courts(self) :
		# fills in the club
		select = Select(driver.find_element_by_name('tennisArrond'))
		select.select_by_visible_text(self.spots[0].club)

		# selects the date
		select = Select(driver.find_element_by_name('dateDispo'))
		select.select_by_value(self.spots[0].date)

		# fills the hour
		hour_input = self.driver.find_element_by_name('heureDispo')
		hour_input.clear()
		hour_input.send_keys(self.spots[0].hour)

		# validates the search
		val_button = self.driver.find_element_by_name('valider')
		val_button.click()

	def book_court(self) :
		success = False
		club = self.spots[0].club
		while (len(self.spots) > 0) and (club == self.spots[0].club) :
			court_no = self.spots[0].court_no
			club = self.spots[0].club
			date_string = to_datetime(self.spots[0].date).strftime('le %A %d %B %Y')
			hour = self.spots[0].hour
			try :
				self.driver.find_element_by_css_selector("a[href*='Court n°{} du tennis {} {} à {}h00']".format(court_no, club, date_string, hour)).click()
				success = True
				return success
			except :
				del self.spots[0]
		return success

if __name__ == '__main__':
	s = Spot('02/11/2017', '12', 'Jules Ladoumègue', 6)
	S = Session(driver, '260294026', '4905', [s])
	S.authenticate()
	S.search_courts()
	S.book_court()
	sleep(5)
	driver.close()

# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# sleep(5)
# assert "No results found." not in driver.page_source
# driver.close()