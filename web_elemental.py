import requests

from lxml import html
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains as ActionChain
from selenium.webdriver.support.ui import WebDriverWait
from utils import load_yaml



class WebElemental():

	def __init__(self, url, driver, yaml_path, delay=40):
		self.url = url
		self.driver = self.select_driver(driver)
		self.delay = delay
		self.wait = WebDriverWait(self.driver, self.delay)
		self.scenario = load_yaml(yaml_path)
		self.start()

	def select_driver(self, driver_name):
		options = {'firefox': webdriver.Firefox()}
		driver_name = driver_name.lower()
		if driver_name in options.keys():
			return options[driver_name]
		else:
			print("\n***That browser is NOT available. Giving you Firefox instead***\n")
		return webdriver.Firefox()

	def start(self):
		self.driver.get(self.url)

	def current_url(self):
		return self.driver.current_url

	def page_status(self, url):
		return requests.get(url).status_code

	def get_page_source(self, url):
		xpathable = html.fromstring(requests.get(url).content) 
		return xpathable

	def get_page_title(self, url):
		source = self.get_page_source(url)
		return source.findtext('.//title')

	def title(self, url):
		return self.driver.title