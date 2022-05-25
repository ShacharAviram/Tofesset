# importing module
import logging
from Constants import *
#THERE ARE 4 MODES THAT WILL BE VALABLE FOR WRITING IN THE LOG
#FILE TO USE EACH MODE WRITE THE FOLLOWING COMMAND 
#self.logger.info("Just an information")
#self.logger.warning("Its a Warning")
#self.logger.error("Did you try to divide by zero")
#self.logger.critical("Internet is down")

# Create and configure logger
def log_creater(file_name):
    logging.basicConfig(filename= DESKTOP_DIR_CONST + file_name + ".log",
					format='%(asctime)s %(message)s',
					filemode='a')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    return logger
if __name__ == "__main__":
    loger = log_creater("test_log")
    loger.info("infooooo")
    loger.warning("warnnnnnnnn")
    loger.error("errorrr")
    