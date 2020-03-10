
from bot import SupremeBot
from supreme import SupremeWeb
import time
import argparse


class MainClass(object):

	def __init__(self):
		pass
	  
	def main(self):

		parser = argparse.ArgumentParser()

		parser.add_argument('-n', '--name', help = "Item Name", type = str)
		parser.add_argument('-c', '--color', help = "Item Color", type = str)
		parser.add_argument('-s', '--size' ,help = "Item Size", type = str, default = '')

		#Parse the command line arguments
		args = parser.parse_args()

		item_name = args.name
		item_color = args.color
		item_size = args.size


		botObject = SupremeBot()
		bot_config = botObject.create_bot() 

		supreme_bot = SupremeWeb(bot_config, item_name = item_name, item_color = item_color, item_size = item_size)
		supreme_bot.start_schedule()
		


if __name__ == '__main__':  
	obj = MainClass();
	obj.main()
	
	