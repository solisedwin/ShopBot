
from bs4 import BeautifulSoup

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import *
from selenium import webdriver

import requests
from lxml.html import fromstring

import re
import  schedule
import random



class SupremeBot(object):

	def __init__(self):
		pass


	def create_bot(self):
		print('-- Creating Bot -- ')
		options = Options()
		#options.headless = True

		proxies = self.proxy_scrap()
		proxy = self.get_proxy_config(proxies)

		#user_agent = self.get_user_agent()

		profile = webdriver.FirefoxProfile()
		profile.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0")

		driver = webdriver.Firefox(options = options, proxy = proxy, firefox_profile = profile)
		driver.set_window_size(690, 650)
		driver.set_window_position(1000, 50)

		return driver


	def proxy_scrap(self):

		url = 'https://free-proxy-list.net/'
		response = requests.get(url)

		parser = fromstring(response.text)
		proxies = set()

		try:
			for i in parser.xpath('//tbody/tr')[:5]:
				if i.xpath('.//td[7][contains(text(),"yes")]'):
					#Grabbing IP and corresponding PORT
					proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
					proxies.add(proxy)

		except Error as e:
			print('~~ Error trying to get proxy')
			print('~~Error: ' + str(e))
		return proxies
		

	def get_proxy_config(self,proxies):

		if(len(proxies) > 0):
			myProxy = proxies.pop()

			proxy = Proxy({
				'proxyType': ProxyType.MANUAL,
				'httpProxy': myProxy,
				'ftpProxy': myProxy,
				'sslProxy': myProxy,
				'noProxy': '' # set this value as desired
			})

			self.proxies = proxies
			return proxy
		else:
			return ''

	def get_user_agent(self):

		user_agent_list = [
			#Chrome
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
			'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
			'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
			'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
			'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
			'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
			'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
			'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',

			#Firefox
			'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
			'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
			'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
			'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
			'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
			'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
			'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
			'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
			'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
			'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
			'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
			'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
			'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
			]


		user_agent = random.choice(user_agent_list)
		# headers = {'User-Agent': user_agent}
		return user_agent

