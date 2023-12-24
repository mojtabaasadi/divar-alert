import os 
os.environ['SEARCH_CONDITIONS'] = "shiraz"
from divar import main
import schedule
import time


schedule.every(10).minutes.do(main)


while 1:
    schedule.run_pending()
    time.sleep(1)