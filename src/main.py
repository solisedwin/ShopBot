

from bot import SupremeBot
from supreme import SupremeWeb
import time


class MainClass(object):

	def __init__(self):
		pass
	  
	
	def main(self):
		botObject = SupremeBot()
		bot = botObject.create_bot() 
		web	= SupremeWeb(bot)



if __name__ == '__main__':  
	
	obj = MainClass();
	obj.main()
	
	   
