import logging
from apscheduler.schedulers.blocking import BlockingScheduler

# Main cronjob function.
from bot import main

#################################
# config
#################################

# logging 
# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

#################################
# cronjob
#################################

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()
scheduler.add_job(main, "interval", hours=1)

scheduler.start()