from airflow.decorators import dag, task
from datetime import datetime

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from controllers.globalScraper import globalScraper
from controllers.elasticSearchController import sources



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),  # Fixed start date
    'retries': 1,
}

@dag(schedule_interval='@daily',  default_args=default_args, catchup=False)
def test():
    sources()



test()
