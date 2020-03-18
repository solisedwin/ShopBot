
import subprocess
import sys
import json
import time

class Bot_Subprocess(object):
	"""docstring for BotSubprocess"""
	def __init__(self):
		pass


	def read_json_clothing_items(self):

		with open('customer.json') as file:
			json_file = json.load(file)
			clothes = json_file	['orders']

			clothing_list = []

			for clothing_article in clothes:
				clothing_article = clothing_article.strip()
				self.site_status = clothing_article.lower()

				for info in clothes[clothing_article]:

					clothing_article = clothing_article.strip()
					name = info['name'].replace(' ', '_').strip()
					color = info['color'].strip()
					size = info['size'].strip()

					#Tuple data structure to perserve/pack clothing information together
					clothing_info = (clothing_article, name, color, size)             
					clothing_list.append(clothing_info)

			file.close()
			return clothing_list


	def config_subprocess(self):
		clothing_list = self.read_json_clothing_items()

		for clothing_info_tuple in clothing_list:	
			article = clothing_info_tuple[0]
			name = clothing_info_tuple[1]
			color = clothing_info_tuple[2]
			size = clothing_info_tuple[3]
			self.run_subprocess(article = article,  name = name, color = color, size = size)


	def run_subprocess(self, article, name , color, size):
	
		article_arg = '-a={}'.format(article)	
		name_arg = '-n={}'.format(name)
		color_arg = '-c={}'.format(color)
		size_arg = '-s={}'.format(size)

		arguments = [article_arg , name_arg , color_arg, size_arg]

		proc = subprocess.Popen(['gnome-terminal', '-x', 'python', 'main.py'] +  arguments)
		proc.wait()



if __name__ == '__main__':
	bot_sub = Bot_Subprocess()  
	bot_sub.config_subprocess()