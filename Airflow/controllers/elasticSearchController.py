from elasticsearch import Elasticsearch, exceptions
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk
from airflow.decorators import task
import hashlib
import base64



HOST = "https://10.10.1.12:9200"
USERNAME = "elastic"
PASSWORD = "elastic"

def get_connection():
    es = Elasticsearch(
            hosts=HOST,
            ca_certs = "/opt/airflow/controllers/ca.crt",
            basic_auth=(USERNAME, PASSWORD),
            verify_certs=True
        )
    return es


def url_to_id(url):
    # Generate SHA-256 hash from the URL
    hash_object = hashlib.sha256(url.encode())
    hash_hex = hash_object.hexdigest()

    # Encode the short hash using Base64
    short_id = base64.urlsafe_b64encode(bytes.fromhex(hash_hex)).decode()
    
    return short_id

def update_source(source, last_execution):
    # connect to ES
    try:
        es = get_connection()
    except:
        print('cant connect to ElasticSearch')
        return False


    try:
        update_body = {
            "doc": {
                "last_execution": last_execution
            }
        }
        response = es.update(index="sources", id=source['id'], body=update_body)
        print(f'editing source {source["name"]}')

    except:
        print(f'failed to editing source {source["name"]}')

@task
def sources():
    # connect to ES
    try:
        es = get_connection()
    except:
        print('cant connect to ElasticSearch')
        return False

    response = es.search(index="sources", body={"query": {"match_all": {}}})
    hits = response['hits']['hits']

    sources = []
    for hit in hits:
        source = {
            'id' : hit['_id'],
            **hit['_source']
        }
        sources.append(source)
    
    return sources 


@task
def store_articles(articles):
    # connect to ES
    try:
        es = get_connection()
    except:
        print('cant connect to ElasticSearch')
        return False
    
    # indexing articles
    for article in articles:

        # generate id
        id = url_to_id(article['url'])

        try:
            es.create(index="articles", id=id, document=article)
            print(f'saving article {id} to ES')

        except:
            print(f"article with ID {id} already exists.")

        


