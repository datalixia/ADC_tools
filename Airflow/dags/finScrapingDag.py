from airflow.decorators import dag, task
from datetime import datetime

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from controllers.globalScraper import globalScraper
from controllers.elasticSearchController import store_articles, sources, update_source


@task()
def check_sources(sources):
    # Filter sources based on the "state" field
    filtered_sources = [source for source in sources if source.get("state") is True]
    valid_sources = []
    current_timestamp = int(datetime.now().timestamp())
    for source in filtered_sources:
        last_execution = source.get("last_execution", 0)
        last_execution = 0
        frequency = source.get("frequency", 0) * 3600  # Convert hours to seconds

        # Check if the source is active
        if source.get("state") is False:
            continue

        # Check if the source has a last execution time
        if last_execution > 0:
            if last_execution + frequency > current_timestamp:
                continue
        
        # update source last_execution timestamp
        update_source(source, current_timestamp)

        # add source to valid sources
        valid_sources.append(source)

    return valid_sources

@task()
def scraper(source):
    scraper = globalScraper(source)
    scraper.run()

    #articles = [{'title': '\n\tScam alert: Scammers impersonating AUSTRAC staff ', 'url': 'https://www.austrac.gov.au/scam-alert-scammers-impersonating-austrac-staff', 'content': '\nA scammer has recently tried impersonating an AUSTRAC official. They emailed members of the public, telling them AUSTRAC had sent documents on their behalf to transfer funds. They also asked them for some business documents.\xa0\nScammers often pretend to be from trusted organisations like AUSTRAC and will seek to appear credible by using a fake website or emails with our logo and branding. They will attempt to trick you into giving out your personal or business information, or to persuade you to make payments or transfer funds.\xa0\nAUSTRAC will never ask you to provide your business details through an online form outside of our AUSTRAC Online portal.\xa0\nIf you think a call, email or message claiming to be from us is not genuine, do not engage with the scammer.\xa0\nReport the incident to\xa0Scamwatch.\nTo find out more about how to spot a scam, visit our\xa0Frauds and scams\xa0page.\nMore information\xa0\nAUSTRAC Contact Centre\xa0information and operating hours.\xa0\nTo find out more about AUSTRAC, visit our\xa0What we do\xa0page.\xa0\nFor concerns about identity theft, contact\xa0IDCARE.\nTips on how to spot a fake website.\xa0\n\n', 'date_time': 1734926400}]
    #return articles
    return scraper.data


@task()
def aggregate_articles(all_articles):
    # Flatten the list of lists into a single list
    merged_articles = [article for sublist in all_articles for article in sublist]
    return merged_articles


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),  # Fixed start date
    'retries': 1,
}

@dag(schedule_interval='@hourly',  default_args=default_args, catchup=False)
def finScraping():
    sources_list = sources()
    filtered_sources = check_sources(sources_list)
    articles = scraper.expand(source=filtered_sources)
    merged_articles = aggregate_articles(articles)
    store_articles(merged_articles)



finScraping()
