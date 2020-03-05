
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

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
- Ingore case for Clothing Item name and color. Change xpath 


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

			for clothing_article in clothes:
			
				clothing_article = clothing_article.strip()
				
				self.load_clothing_page(clothing_article)

				for info in clothes[clothing_article]:

					name = info['name'].strip()
					color = info['color'].strip()
					size = info['size'].strip()

					#Tuple data structure to perserve/pack clothing information together
					clothing_info = (name, color, size)				
					self.search_match_clothes(clothing_info)
				
					

			self.checkout_items()
				
			  


	def is_kicked_out(self):
		current_url = self.driver.current_url

		#We are kicked out of page. Website error due to traffic
		if 'out_of_stock' in current_url or '/shop/all' not in current_url:
			schedule.every(3).seconds.do(self.access_home_site).tag('kicked-out')   
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
	


	def search_match_clothes(self, clothing_info):	

		clothing_name = clothing_info[0]
		clothing_color = clothing_info[1]
		clothing_size = clothing_info[2]

		item_xpath_locator = '//div[@class="inner-article" and .//*[contains(text(), "{}")] and .//*[contains(text(), "{}")]]'.format(clothing_name, clothing_color)
			

		print("Looking at " + str(clothing_name) + " with color " + str(clothing_color) + " at size " + str(clothing_size))


		try:
			
			supreme_item_div = self.driver.find_element_by_xpath(item_xpath_locator)            
			self.driver.execute_script("arguments[0].scrollIntoView(true);", supreme_item_div);

			self.driver.execute_script("arguments[0].setAttribute('data-selected-item','item-looking-at')", supreme_item_div)
			
			#Hover over clothing item we are looking at, to see if sold_out_tag is present and shows up in the DOM 
			hover = ActionChains(self.driver).move_to_element(supreme_item_div).perform()
			
			sold_out_tag = self.driver.find_element_by_xpath('//div[@data-selected-item="item-looking-at" and //div[@class = "sold_out_tag"]]')
			tag_text = str(sold_out_tag.text)

			self.driver.execute_script("arguments[0].removeAttribute('data-selected-item')", sold_out_tag)

			if 'sold out' in tag_text:
				print("~~ Item is sold out ")
			else:				
				
				self.add_to_cart(sold_out_tag)
				self.driver.back()
				self.driver.refresh();
		except Exception as e:
			print('~~ 	Error: ' + str(e))



	def add_to_cart(self, sold_out_tag):

		self.click_item(sold_out_tag)

		wait = WebDriverWait(self.driver, self.delay)
		wait.until(EC.element_to_be_clickable((By.ID, "details")))      
		
		add_to_cart_btn = self.driver.find_element_by_css_selector('#add-remove-buttons > input');              
	
		action = ActionChains(self.driver)
		hov = action.move_to_element(add_to_cart_btn).click().perform
		
		wait.until(EC.presence_of_element_located((By.ID, "cart")))
		print('** Added item to cart ** ')
		print()

		

	def click_item(self, item):
		action = ActionChains(self.driver)
		action.click(item).perform()


	def process_payment(self, action):
		payment_btn = self.driver.find_element_by_css_selector('input.button')
		action.move_to_element(payment_btn).click().perform() 


	def checkout_items(self):

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






