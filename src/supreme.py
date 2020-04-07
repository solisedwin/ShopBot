
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
from datetime import datetime

import schedule
import random
import requests
import json
import sys

class SupremeWeb(object):

    def __init__(self, driver, item_clothing_article , item_name, item_color, item_size):
        self.driver = driver
        self.delay = 20

        #Init value when we start at the home page
        self.site_status = "supremenewyork"

        self.clothing_article = item_clothing_article

        self.item_name = item_name
        self.item_color = item_color
        self.item_size = item_size


    def start_schedule(self):
        print('------ Waiting for exact time to run bot --------')

        schedule.every().thursday.at("11:00").do(self.checking_site_access , first_time_access = True)

        self.run_schedule()


    def run_schedule(self):
        while True:
            schedule.run_pending()
            time.sleep(1)


    def checking_site_access(self, first_time_access = False):

        current_url = self.driver.current_url
        clothing_article_url =  "https://www.supremenewyork.com/shop/all/{}".format(self.clothing_article)

        url = clothing_article_url if first_time_access else current_url
        request = requests.get(url)

        if request.status_code != 200:
            print('~~ 200 Status code error. Site cant be loaded. Trying again')
            self.driver.implicitly_wait(1)
            self.checking_site_access(first_time_access = first_time_access)

        #We were kicked out of website probably due to high traffic/bot detection. Run again from home page
        elif 'out_of_stock' in current_url or (self.site_status not in current_url and not first_time_access):
            print('### Kicked out of web site !!! ###')
            self.driver.implicitly_wait(1)
            self.run_bot()
        elif first_time_access:
            print('@@ Entering Supreme Site @@')
            self.run_bot()
        else:
            #We are in the middle of running the bot now. No errors (kicked out) have been made
            print('* Havent been kicked out, still running fine *')


    def is_kicked_out(self):
        current_url = self.driver.current_url

        #We are kicked out of page. Website error due to traffic
        if 'out_of_stock' in current_url or self.site_status not in current_url:
            print('##### Kicked out of web site! ######')
            schedule.every(3).seconds.do(self.checking_site_access).tag('kicked-out')
        else:
            print('Not kicked out yet')


    def run_bot(self):

        schedule.every(4).seconds.do(self.checking_site_access, first_time_access = False)

        clothing_info = (self.item_name, self.item_color, self.item_size)
        self.load_clothing_page(self.clothing_article)

        #Get current time to always refresh site in case item isnt founded yet.
        currentDT = datetime.now()

        self.search_match_clothes(clothing_info, previous_time_minute = currentDT.minute)



    def load_clothing_page(self, clothing_article):

        url = "https://www.supremenewyork.com/shop/all/{}".format(clothing_article)
        self.driver.get(url)
        wait = WebDriverWait(self.driver, self.delay)
        wait.until(EC.presence_of_element_located((By.ID, "container")))

        self.site_status = clothing_article


    def search_match_clothes(self, clothing_info, previous_time_minute,):

        clothing_name = clothing_info[0].replace('_',' ')
        clothing_color = clothing_info[1]
        clothing_size = clothing_info[2]

        item_xpath_locator = '//div[@class="inner-article" and .//*[contains(text(), "{}")] and .//*[contains(text(), "{}")]]'.format(clothing_name, clothing_color)

        print("Looking at " + str(clothing_name) + " with color " + str(clothing_color) + " at size " + str(clothing_size))

        try:
            supreme_item_div = self.driver.find_element_by_xpath(item_xpath_locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", supreme_item_div);

            #Click item to see if sold out button is shown, if shown: exit program. Else: continue to checkout item
            hover = ActionChains(self.driver).click(supreme_item_div).perform()
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(EC.element_to_be_clickable((By.ID, "details")))

            sold_out = self.is_sold_out()

            if sold_out:
                print("~~ Item is sold out :( ")
                self.driver.quit()
                sys.exit(1)
            else:
                self.add_to_cart()
                self.edit_cart_items()
                self.read_pay_json_paymentinfo()

        except NoSuchElementException as no_element:

            current_time = datetime.now()
            current_time_minute = current_time.minute
            #We only allow refreshing to find item, for 3 mintues
            if(current_time_minute == previous_time_minute + 3 ):
                print('~~ Cant find element {} {} after 3 extra minutes. Closing application'.format(clothing_name, clothing_color))
                time.sleep(4)
                self.driver.quit()
                sys.exit(1)
            else:
                print('~~ Element cant be found. Refreshing website to check again')
                self.driver.refresh()
                self.search_match_clothes(clothing_info, previous_time_minute)

        except Exception as e:
            print('~~ Error: ' + str(e))


    def is_sold_out(self):

        try:
            sold_out_tag = self.driver.find_element_by_css_selector('b.sold-out')
            #Item is sold out
            if sold_out_tag:
                return True
            else:
                return False
        except NoSuchElementException as no_sold_out_tag:
            return False


    def add_to_cart(self):

        try:
            add_to_cart_btn = self.driver.find_element_by_css_selector('#add-remove-buttons > input');

            action = ActionChains(self.driver)
            hov = action.move_to_element(add_to_cart_btn).click().perform()

            #wait.until(EC.presence_of_element_located((By.ID, "cart")))
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "in-cart")))
            print('** Added item to cart ** \n')

        except TimeoutException as e:
            print('~~ Timeout Exception. Element isnt being added to cart')
            self.add_to_cart(item)


    def click_item(self, item):
        action = ActionChains(self.driver)
        action.click(item).perform()


    def edit_cart_items(self):

    	self.driver.get("https://www.supremenewyork.com/shop/cart")

    	out_of_stock_items = self.driver.find_elements_by_css_selector('tr.out_of_stock')

    	#Have to remove items
    	if (len(out_of_stock_items) > 0):
    		pass






    # Read JSON file with user's card information, while also in payment page
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

        print('------ Check out page -------')

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
            print("@@ Too much time has passed to checkout/load payment page @@")
            self.checkout_items(payment_information, dropdown_payment_info)


    def confirmation_page(self):

        # Wait for 6 mintues for confirmation payment page. At this point, we arent sure if order failed or sucessful went through
        confirmation_wait = WebDriverWait(self.driver, 60 * 10)
        confirmation_wait.until(EC.presence_of_element_located((By.ID, 'confirmation')))

        has_failed_confirmation =  bool(self.driver.find_element_by_xpath('//div[contains(@class,"failed")]'));

        if(has_failed_confirmation):
            self.driver.back()
        else:
            self.driver.implicitly_wait(15)
            self.driver.quit()
            sys.exit(1)


    def click_payment_button(self, action):
        payment_btn = self.driver.find_element_by_css_selector('input.button')
        action.move_to_element(payment_btn).click().perform()
