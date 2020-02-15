
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select

from selenium.webdriver.common.proxy import *   

from bs4 import BeautifulSoup 
from urllib.request import Request, urlopen

import time
import schedule
import random
import requests



"""
TODO:
-Loading takes too much time or cant find element (handle error)
"""

class Supreme(object):


	def __init__(self, tasks, proxies):

		schedule.every(3).seconds.do(self.access_to_site).tag('kicked-out')	
		
		self.tasks = tasks

		options = Options()
		options.headless = True

		proxy = self.get_proxy_config(proxies)

		user_agent = self.get_user_agent()

		profile = webdriver.FirefoxProfile()
		profile.set_preference("general.useragent.override", user_agent)

		self.driver = webdriver.Firefox(options = options, proxy = proxy, firefox_profile = profile)
		self.delay = 3.1
		self.url = ''



	def access_to_site(self):		
		request = requests.get('https://www.supremenewyork.com/shop/all')
		if request.status_code == 200:
			print('Web site is now open for shopping!')
			schedule.clear('kicked-out')
			self.run_tasks()
		else:
			print('Supreme site isnt open now') 
		



	def is_kicked_out(self):
		#Current url page we are in now
		if 'out_of_stock' in self.driver.current_url:
			schedule.every(3).seconds.do(self.access_to_site).tag('kicked-out')	
		else:
			print('Not kicked out yet')



	def run_schedule(self):
		while True:
			schedule.run_pending()
			time.sleep(1)




	def run_tasks(self):
		schedule.every(4).seconds.do(self.is_kicked_out)
		
		# KEY: (t-shirts, pants, jeans...etc)
		for key in self.tasks:

			self.url  = "https://www.supremenewyork.com/shop/all/{clothing}".format(clothing = key)
			self.load_clothing_page(self.url)
			self.locate_clothes(key);


		self.checkout_item()
		# self.driver.close()		
	 		


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
	


	def load_clothing_page(self, url):

		self.driver.get(url)

		wait = WebDriverWait(self.driver, self.delay)
		wait.until(EC.presence_of_element_located((By.ID, "container")))
	


	def locate_clothes(self, key):
	
		clothing_names =  lambda:  self.driver.find_elements_by_css_selector('.product-name > a')
		color_items = lambda : self.driver.find_elements_by_css_selector('.product-style > a')
	
	
		items_length = len(clothing_names())

		#Connect clothing name and color together, to check values only once
		for index in range(items_length):

			#r key (t-shirts, hats, pants, ...) is emoty without any clothing brand names. Exit loop for this key
			if not self.tasks[key]:
				break


			name = clothing_names()[index]		
			color = color_items()[index]

			name_txt = name.text.lower().strip()
			color_txt = color.text.lower().strip()

			print(name_txt + ' ' + color_txt)

			if (name_txt in self.tasks[key] and color_txt in self.tasks[key][name_txt]):
				print('Found a match. Keyword: ' + name.text + ' Color ' + color.text)  			
				
				#Removes color from set
				self.tasks[key][name_txt].discard(color_txt)

				#If article clothing name is empty, remove from key dict
				if not self.tasks[key][name_txt]:
					#self.tasks[key].pop(name_txt)
					del self.tasks[key]

				#Add ID to a/(href) tag. So we can access it quick and traverse the nodes
				self.driver.execute_script("arguments[0].setAttribute('id','name-link-id')", name)
			
				#Pass a web service object as 'name'
				if(self.is_item_sold_out(name, 'name-link-id')):
					#item is sold out
					print('## Item is sold out ##')
					continue
				else:
					#Click item from shop/all page
					self.click_item(name)
					self.add_to_cart()

					print("\n ** Added {name} {color} to cart ** ".format(name = name_txt, color = color_txt))
					self.driver.back()
					self.driver.refresh();
					
					continue
			else:
				pass
	



	def process_payment(self, action):
		payment_btn = self.driver.find_element_by_css_selector('input.button')
		action.move_to_element(payment_btn).click().perform()   



	def checkout_item(self):

		#Redirect to process page
		self.driver.get('https://www.supremenewyork.com/checkout')

		# Inputing for all input tags
		print('Item(s) has been checked out. We are PAYING for it now')

		input_data = ['fake name', 'fake_email10@aol.com', '1111111111', '78 cat street', '3L', '12345', 'Oniondale', '5412 7543 5678', '503']

		wait = WebDriverWait(self.driver, 4)
		wait.until(EC.presence_of_element_located((By.ID, "cart-body")))


		#All input tags
		input_tags = self.driver.find_elements_by_css_selector('input.string')
	
		
		for index,tag in enumerate(input_tags):
			tag.send_keys(input_data[index])

		
		select_data = ['NY','USA', '10', '2022']

		#Select choices for select tags 
		select_tags = self.driver.find_elements_by_css_selector('select')
		action = ActionChains(self.driver)


		for index, tag in enumerate(select_tags):

			element = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.ID, tag.get_attribute("id"))))		   
			action.move_to_element(element)
			
			select = Select(element)
			select.select_by_value(select_data[index])


		action.click(self.driver.find_elements_by_css_selector('.iCheck-helper')[1]);
		
		self.driver.implicitly_wait(1)
		self.process_payment(action)




	def add_to_cart(self):
	
		wait = WebDriverWait(self.driver, self.delay)
		wait.until(EC.element_to_be_clickable((By.ID, "details")))      
		

		add_to_cart_btn = self.driver.find_element_by_css_selector('#add-remove-buttons > input');              
	
		action = ActionChains(self.driver)
		hov = action.move_to_element(add_to_cart_btn)
		hov.click().perform()
	
		wait.until(EC.presence_of_element_located((By.ID, "cart")))

		

	def click_item(self, item):
		action = ActionChains(self.driver)
		action.click(item).perform()



	def is_item_sold_out(self,item_to_hover, name):

		try:
			x = item_to_hover.location['x']
			y = item_to_hover.location['y']

			scroll_by_coord = 'window.scrollTo(%s,%s);' % (x,y)
			self.driver.execute_script(scroll_by_coord)

			#If sold out tag exists on outer item div, then the item is no longer in stock. 
			sold_out_tag = self.driver.find_element_by_xpath('//a[@id = "name-link-id"]/../..//div[@class = "sold_out_tag"]');
			return True

		except Exception as e:
			return False
