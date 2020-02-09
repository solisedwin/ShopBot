
from bs4 import BeautifulSoup 
from Supreme import Supreme
import sys
import re
import time

import requests
from lxml.html import fromstring

import time, schedule
		 

class WebCalls(object):

	def __init__(self):

	   self.proxies =  self.proxy_scrap()
	   self.tasks = dict()
	   self.items = 0


	def get_keywords(self):

		regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]') 

		while True:

			print('\n' + str(self.items) + ' items added') 
			print ('Structure: t-shirts, name, color')
			print ('Example: t-shirts, bridge tee, slate')
			print('Enter "Run", to execute all tasks. If not, keep putting items to search')

			keywords = input('Enter word keywords: ').lower().strip()
			hasNumber = any(char.isdigit() for char in keywords)

			if(hasNumber) or not regex.search(keywords) == None:
				print ('Keywords cant contain any digit or special characters. Enter again')
				continue
			elif not keywords:
				print('Error !! Input is empty spaces.')
				continue
			elif 'run' in  keywords:
				print('\n--- Input has been processed. ---')
				self.run_supreme_bot()
				break
			elif keywords.count(',') != 2:
				print('Bad input ! See Example ontop.')
			else:

				keywords = keywords.split(',')
				clothing_article = keywords[0].strip()
				item_name = keywords[1].strip()
				item_color = keywords[2].strip()

				#t-shirts for instance, hasnt at all be made
				if clothing_article not in self.tasks:
					self.tasks[clothing_article] = dict()
					self.tasks[clothing_article][item_name] = set()
					self.tasks[clothing_article][item_name].add(item_color)

				elif clothing_article in self.tasks and item_name not in self.tasks[clothing_article]:
					self.tasks[clothing_article][item_name] = set()
					self.tasks[clothing_article][item_name].add(item_color)
				else:
					self.tasks[clothing_article][item_name].add(item_color)
			self.items += 1   



	def websiteChoice(self):

		choices = [1,2]

		choice = 0;

		while True: 
				
			print('1.) Supreme New York')
			print('2.) Exit program')

			websiteNumber = input('Enter website number you want to shop from: ').strip()

			if not websiteNumber.isnumeric():
				print ('\nNot a number!')
				continue
			elif eval(websiteNumber) not in choices:
				print ('\nNot a valid choice. Enter website number')
				continue;

			elif eval(websiteNumber) == 1:
				print ('----- You choose Supreme New York -----')  
				choice = 1;
				self.get_keywords()
				break;

			elif eval(websiteNumber) == 2:
				sys.exit('Exited program')
			else:
				continue


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



	def run_supreme_bot(self):
		start_time = time.time()        
	
		supreme = Supreme(self.tasks,self.proxies)
		supreme.run_schedule()

		print ('\n *****************************')  
		print('Suprmeme bot runtime: ' + str(time.time() - start_time));




if __name__ == '__main__':  
	
	obj = WebCalls();
	obj.websiteChoice()
	
	   
