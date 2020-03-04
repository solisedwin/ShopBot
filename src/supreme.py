
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
import json
import sys


"""
TODO:
-Loading takes too much time or cant find element (handle error)
- Ingore case for Clothgin Item name and color. Change xpath 


('//div[@class="inner-article" and //*//text()[contains(translate(.,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"), "Bling Tee")] 
and //*//text()[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"Red")] ]')


"""

class SupremeWeb(object):

	def __init__(self, driver):

		self.driver = driver
		self.delay = 3.5
		"""
		#schedule.every().thursday.at("11:00").do(self.run_bot)
		print('-- Waiting for 11:00 AM ono Thursday --')
		"""
		self.run_bot()
		self.run_schedule()


	def access_home_site(self):     
		request = requests.get('https://www.supremenewyork.com/shop/all/')
		if request.status_code == 200:
			print('Web site is now open for shopping!')
			schedule.clear('kicked-out')
			self.run_bot()
		else:
			print('Supreme site isnt open now') 



	def run_bot(self):

		#schedule.every(4).seconds.do(self.access_home_site).tag('kicked-out')   
		schedule.every(3.5).seconds.do(self.is_kicked_out)
		# self.run_schedule()
		self.json_clothing_orders()
		#self.driver.close()        



	def json_clothing_orders(self):

		with open('customer.json') as file:
			json_file = json.load(file)
			clothes = json_file['orders']

			for item in clothes:
				clothing_article = item.strip()
				clothing_information_list = []

				for info in clothes[clothing_article]:

					name = info['name'].strip()
					color = info['color'].strip()
					size = info['size'].strip()

					#Tuple data structure to perserve/pack clothing information together
					clothing_info = (clothing_article, name, color, size)

					""" 
					List is made so that we have all the article clothing values together. In order to look through clohthing-article page ONCE
					Also, to avoid heavy computation for each iteration
					"""

					clothing_information_list.extend(clothing_info)

				self.search_match_clothes(clothing_information_list)


			#self.checkout_item()
				
			  


	def is_kicked_out(self):
		current_url = self.driver.current_url

		#We are kicked out of page. Website error due to traffic
		if 'out_of_stock' in current_url or '/shop/all' not in current_url:
			schedule.every(2).seconds.do(self.access_home_site).tag('kicked-out')   
		else:
			print('Not kicked out yet')



	def run_schedule(self):
		while True:
			schedule.run_pending()
			time.sleep(1)


			
	def load_clothing_page(self, clothing_article):

		url = "https://www.supremenewyork.com/shop/all/{}".format(clothing_article)

		self.driver.get(url)

		wait = WebDriverWait(self.driver, self.delay)
		wait.until(EC.presence_of_element_located((By.ID, "container")))
	



	def search_match_clothes(self, clothing_info_list):

		clothing_article = clothing_info_list[0]
		self.load_clothing_page(clothing_article)

		clothing_name = clothing_info_list[1]
		clothing_color = clothing_info_list[2]
		clothing_size = clothing_info_list[3]

		item_xpath_locator = '//div[@class="inner-article" and .//*[contains(text(), "{}")] and .//*[contains(text(), "{}")]]'.format(clothing_name, clothing_color)
		
		print("Looking at " + str(clothing_name) + " with color " + str(clothing_color) + " at size " + str(clothing_size))

		try:
			supreme_item_div = self.driver.find_element_by_xpath(item_xpath_locator)            
			self.driver.execute_script("arguments[0].setAttribute('data-selected-item','item-looking-at')", supreme_item_div)
		
			is_sold_out = self.is_item_sold_out(item_to_hover =  supreme_item_div)
			sys.exit(1)

			if(is_sold_out):
				print('*** Item is sold out ! ***')
			else:   
				self.click_item(supreme_item_div)
				self.add_to_cart()
				self.driver.back()
				self.driver.refresh();
		except Exception as e:
			print("~~Error. " + str(e))



	def is_item_sold_out(self,item_to_hover):

		try:
			x = item_to_hover.location['x']
			y = item_to_hover.location['y']

			scroll_by_coord = 'window.scrollTo(%s,%s);' % (x,y)
			self.driver.execute_script(scroll_by_coord)
			#If sold out tag exists on outer item div, then the item is no longer in stock. 
			sold_out_tag_exist = self.driver.find_element_by_xpath('boolean(//div[@data-selected-item = "item-looking-at"]/a/div[contains(@class, "sold_out_tag")])');
			print('Type: ' + str(type(sold_out_tag_exist)))
			sys.exit(1)

			if sold_out_tag_exist:
				return True
			else:
				return False
				
		except Exception as e:
			print('~~ Exception in is_item_sold_out fun: ' + str(e))
			return False



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
		print('* Added item to cart ** ')
		print()

		

	def click_item(self, item):
		action = ActionChains(self.driver)
		action.click(item).perform()



