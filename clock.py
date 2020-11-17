import logging
from apscheduler.schedulers.blocking import BlockingScheduler

# Main cronjob function.
from bot import main

#################################
# config
#################################

run_period_in_minutes = 30

# logging 
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

#################################
# cronjob
#################################

def cronjob():

    # Create an instance of scheduler and add function.
    scheduler = BlockingScheduler()
    scheduler.add_job(main, "interval", minutes=run_period_in_minutes)

    scheduler.start()

if __name__ == "__main__":
    cronjob()