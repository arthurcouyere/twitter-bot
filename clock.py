import logging
from apscheduler.schedulers.blocking import BlockingScheduler

# Main cronjob function.
from bot import main

#################################
# config
#################################

# logging 
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

#################################
# cronjob
#################################

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()
scheduler.add_job(main, "interval", minutes=30)

scheduler.start()
