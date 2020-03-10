
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

	def __init__(self, driver, item_name, item_color, item_size):
		self.driver = driver
		self.delay = 20
		self.current_payment_total = 0
		self.max_spending_cost = 0
		#Init value when we start at the home page
		#self.site_status = "supremenewyork"

		self.item_name = item_name
		self.item_color = item_color
		self.item_size = item_size


	def start_schedule(self):
		print('------ Waiting for exact time to run bot --------')
		schedule.every().tuesday.at("01:15").do(self.access_home_site)
		self.run_schedule()


	def run_schedule(self):
		while True:
			schedule.run_pending()
			time.sleep(1)

		
	def access_home_site(self):    

		self.site_status = "supremenewyork"

		request = requests.get('https://www.supremenewyork.com/shop/all/')
		if request.status_code == 200:
			print('Web site is now open for shopping!')
			schedule.clear('kicked-out')
			schedule.every(3.5).seconds.do(self.is_kicked_out) 		
			self.run_bot()
		else:
			print('Supreme site isnt open now') 


	def is_kicked_out(self):
		current_url = self.driver.current_url

		#We are kicked out of page. Website error due to traffic
		if 'out_of_stock' in current_url or self.site_status not in current_url:
			print('##### Kicked out of web site! ######')
			schedule.every(1.5).seconds.do(self.access_home_site).tag('kicked-out')   
		else:
			print('Not kicked out yet')


	def run_bot(self):
		# self.run_schedule()
		
		clothing_info = (self.item_name, self.item_color, self.item_size)
		self.search_match_clothes(clothing_info)
		self.read_pay_json_paymentinfo() 


		"""
		self.read_run_clothing_orders()
		Close entire application
		self.driver.close()       
		sys.exit(1)
		"""

	def read_run_clothing_orders(self):

		with open('customer.json') as file:
			json_file = json.load(file)
			#self.max_spending_cost = int(json_file['max_spending_cost'])

			clothes = json_file	['orders']

			for clothing_article in clothes:
			
				"""
				if (self.current_payment_total >= self.max_spending_cost):
					print("--- Exceed max amount of spending. Now preceding to checkout ---")
					break	
				"""

				clothing_article = clothing_article.strip()
				self.load_clothing_page(clothing_article)

				self.site_status = clothing_article.lower()

				for info in clothes[clothing_article]:

					name = info['name'].strip()
					color = info['color'].strip()
					size = info['size'].strip()

					#Tuple data structure to perserve/pack clothing information together
					clothing_info = (name, color, size)             
		
				self.search_match_clothes(clothing_info)	

			file.close()
			self.read_pay_json_paymentinfo()    
					 

			
	def load_clothing_page(self, clothing_article):

		url = "https://www.supremenewyork.com/shop/all/{}".format(clothing_article)

		self.driver.get(url)
		wait = WebDriverWait(self.driver, self.delay)
		wait.until(EC.presence_of_element_located((By.ID, "container")))
	

	def search_match_clothes(self, clothing_info):  

		clothing_name = clothing_info[0].replace('_',' ')
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
				"""
				self.driver.back()
				self.driver.refresh();
					"""	
		
		except NoSuchElementException as no_element:
			print('~~ Element cant be found. Perhaps has been removed from website')
		except Exception as e:
			print('~~ Error: ' + str(e))



	def add_to_cart(self, item):

		self.click_item(item)
		
		wait = WebDriverWait(self.driver, self.delay)
		wait.until(EC.element_to_be_clickable((By.ID, "details")))      
		"""
		if( self.does_item_exceed_spending_amount() ):
			print("$$$ Adding item would exceeds maximum spending amount of {} ! Cant be added $$$".format(self.max_spending_cost))
		else: 
		"""
		add_to_cart_btn = self.driver.find_element_by_css_selector('#add-remove-buttons > input');              
		
		action = ActionChains(self.driver)
		hov = action.move_to_element(add_to_cart_btn).click().perform()

		#wait.until(EC.presence_of_element_located((By.ID, "cart")))
		wait.until(EC.presence_of_element_located((By.CLASS_NAME, "in-cart")))
		
		print('** Added item to cart ** ')
		print()

		
	def click_item(self, item):
		action = ActionChains(self.driver)
		action.click(item).perform()

	
	"""
	def does_item_exceed_spending_amount(self):
		
		item_cost = self.driver.find_element_by_xpath("//span[@data-currency='USD']")
		#Remove dollar sign $
		item_cost_value = int(item_cost.text[1 : ])
		
		if ( item_cost_value + self.current_payment_total > self.max_spending_cost  ):
			return True
		else:
			self.current_payment_total += item_cost_value
			return False
	"""


	def read_pay_json_paymentinfo(self):
		with open('customer.json') as file:

			json_file = json.load(file) 	

			customer_info = json_file['payment']

			name = customer_info['name']
			email = customer_info['email']
			phone = customer_info['phone']
			address = customer_info['address']
			apt_num = customer_info['apt_num']
			zip_code = customer_info['zip']
			town_name = customer_info['town']
			card_num  = customer_info['card']
			cvv_num = customer_info['cvv']

			payment_information = (name, email, phone, address, apt_num,  zip_code, town_name , card_num, cvv_num)

			state = customer_info["state"]
			country = customer_info["country"]
			card_expiration_month = customer_info["card_expiration_month"]
			card_expiration_year = customer_info["card_expiration_year"]

			dropdown_payment_info = (state, country, card_expiration_month, card_expiration_year)

			self.checkout_items(payment_information, dropdown_payment_info)
			file.close()


	def checkout_items(self, payment_information, dropdown_payment_info):

		#Redirect to process page
		self.driver.get("https://www.supremenewyork.com/checkout")
		self.site_status = "checkout"

		time.sleep(1)

		try:
			wait = WebDriverWait(self.driver,self.delay)
			wait.until(EC.presence_of_element_located((By.ID, "cart-body")))
			#All input tags
			input_tags = self.driver.find_elements_by_css_selector('input.string')

			for index,tag in enumerate(input_tags):
				tag.send_keys(payment_information[index])

			#Select choices for select tags 
			select_tags = self.driver.find_elements_by_css_selector('select')
			action = ActionChains(self.driver)


			for index, tag in enumerate(select_tags):
				element = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.ID, tag.get_attribute("id"))))        
				self.driver.execute_script("arguments[0].click();", element)


			# Check terms and agreement button
			action.click(self.driver.find_elements_by_css_selector('.iCheck-helper')[1]);
			self.click_payment_button(action)

			#self.confirmation_page()

		except TimeoutException as e:
			print("@@ Too much time has passed to checkout/load payment page")
			self.checkout_items(payment_information, dropdown_payment_info)

		#self.has_confirmation_error()	

	
	def has_confirmation_error(self):
		
		wait = WebDriverWait(self.driver,self.delay)
		confirmation_tab = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "selected")]/b[text()="CONFIRMATION"]')))

		failed_card_message = self.driver.find_element_by_css_selector(".failed")
		self.driver.back()



	def click_payment_button(self, action):
		payment_btn = self.driver.find_element_by_css_selector('input.button')
		action.move_to_element(payment_btn).click().perform() 