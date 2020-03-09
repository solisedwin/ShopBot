from bot import SupremeBot
from supreme import SupremeWeb
import time

class MainClass(object):

	def __init__(self):
		pass
	  
	
	def main(self):
		botObject = SupremeBot()
		bot_config = botObject.create_bot() 
		surpeme_bot = SupremeWeb(bot_config)

		surpeme_bot.start_schedule()



if __name__ == '__main__':  
	
	obj = MainClass();
	obj.main()
	
	   
