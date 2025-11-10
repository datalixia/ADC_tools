from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch, exceptions
from pydantic import BaseModel
from typing import Optional
from collections import defaultdict
from datetime import datetime


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5010",
    "10.10.1.20:5010"
    "api:5010"
    "10.10.1.11:5001"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)


class PostsQuery(BaseModel):
    sources: Optional[list[str]] = None
    search: Optional[str] = None 
    start_date: Optional[int] = None
    end_date: Optional[int] = None
    sort: Optional[str] = 'By date'
    size: int = 40
    page: int = 0

class SourceQuery(BaseModel):
    source: dict


class PostQuery(BaseModel):
    post_id: str


class SourceStatsQuery(BaseModel):
    sources: Optional[list[str]] = None
    start_date: Optional[int] = None
    end_date: Optional[int] = None

HOST = "https://10.10.1.12:9200"
USERNAME = "elastic"
PASSWORD = "elastic"

def get_connection():
    # connect to ES
    es = Elasticsearch(
            hosts=HOST,
            ca_certs = "/code/app/ca.crt",
            basic_auth=(USERNAME, PASSWORD),
            verify_certs=True
        )
    return es


def aggregations(data):
    # Dictionary to hold aggregated data
    aggregated = defaultdict(int)

    # Process each item
    for item in data:
        # Convert timestamp to date string
        date_str = datetime.utcfromtimestamp(item["timestamp"]).strftime('%Y-%m-%d')
        # Aggregate the count
        aggregated[date_str] += item["count"]

    # Convert to list of dicts if needed
    result = [{"date": date, "count": count} for date, count in sorted(aggregated.items())]

    if len(result) > 9:
        result = result[-9:]

    return result
    



@app.get("/create_source_index")
def create_source_index():

    try:
        es = get_connection()
    except:
        print('cant connect to ElasticSearch')
        return False
    
    index_name = "sources"
    #es.indices.delete(index=index_name, ignore=[400, 404])
    #return es.info()

    # Check if the index already exists
    if not es.indices.exists(index=index_name):
        # Create index
        es.indices.create(index=index_name)
        return(f"Index '{index_name}' created successfully!")
    else:
        return(f"Index '{index_name}' already exists.")

@app.get("/add_source")
def add_source(name: str = '', url: str = '', state: bool = True, frequency: int = 6):

    try:
        es = get_connection()
        # Confirm connection
        if not es.ping():
            print("Connection established, but cluster is not responding to ping.")
            return False
    except exceptions.ConnectionError as e:
        return {"error": "Can't connect to Elasticsearch", "details": str(e)}
    except exceptions.ElasticsearchException as e:
        return("Elasticsearch error:", e)

    source = {
        "name": name,
        "url": url,
        "state": state,
        "frequency": frequency,
        "last_execution" : 0,
    }
    
    try:
        response = es.index(index="sources", document=source)
        return {"message": "Document added", "id": response['_id']}
    except exceptions.ConnectionTimeout as e:
        return("Indexing timeout:", e)
    except exceptions.ElasticsearchException as e:
        return("Error indexing document:", e)
    
@app.post("/source/edit")
def edit_source(query : SourceQuery):
    try:
        es = get_connection()
    except:
        return {
            "error" : "cant connect to elasticsearch"
        }
    index_name = "sources"

    # update source by id
    source_id = query.source['id']

    response = es.update(index="sources", id=source_id, doc={"frequency": int(query.source['frequency']), "state": query.source['state']})

    if response['result'] == 'updated' or response['result'] == 'noop':
        return {
            "message" : "source updated",
            "id" : source_id
        }
    else:
        return {
            "error" : True,
            "message" : "cant update source"
        }


@app.post("/sources/chart")
def sources_stats(query : SourceStatsQuery):

    try:
        es = get_connection()
    except:
        return {
            "error" : "cant connect to elasticsearch"
        }

    index_name = "articles"

    aggs = {
             "timestamp_count": {
                "terms": {
                    "field": "date_time",
                    "size": 1000,
                }
            }
    }

    # range query 
    range_query = None
    if query.start_date is not None:
        range_query = {
            "range": {
                "date_time": {
                    "gte": query.start_date,
                }
            }
        }
    
    if query.end_date is not None:
        if range_query is None:
            range_query = {
                "range": {
                    "date_time": {
                        "lte": query.end_date,
                    }
                }
            }
        else:
            range_query['range']['date_time']['lte'] = query.end_date


    query = {
            "bool": {
                "filter": [
                    
                        range_query
                    
                ]
            }
    }

    response = es.search(
    index=index_name,  
    size=0,
    query = query,
    aggs = aggs)

    sources = []
    for bucket in response['aggregations']['timestamp_count']['buckets']:
        sources.append({
            "timestamp" : bucket['key'],
            "count" : bucket['doc_count']
        })

    
    return aggregations(sources)



@app.post("/sources/stats")
def sources_stats(query : SourceStatsQuery):
    try:
        es = get_connection()
    except:
        return {
            "error" : "cant connect to elasticsearch"
        }

    index_name = "articles"
    aggs = {
            "source_name_count": {
                "terms": {
                    "field": "source_name.keyword",  # Use ".keyword" for exact match
                    "size": 1000  # Increase if you expect more unique source_name values
                }
            }
    }

    # range query 
    range_query = None
    if query.start_date is not None:
        range_query = {
            "range": {
                "date_time": {
                    "gte": query.start_date,
                }
            }
        }
    
    if query.end_date is not None:
        if range_query is None:
            range_query = {
                "range": {
                    "date_time": {
                        "lte": query.end_date,
                    }
                }
            }
        else:
            range_query['range']['date_time']['lte'] = query.end_date


    query = {
            "bool": {
                "filter": [
                    
                        range_query
                    
                ]
            }
    }
    response = es.search(
    index=index_name,  
    size=0,
    query = query,
    aggs = aggs)

    sources = []
    for bucket in response['aggregations']['source_name_count']['buckets']:
        sources.append({
            "source_name" : bucket['key'],
            "count" : bucket['doc_count']
        })
    print(sources)
    return sources

@app.get("/sources")
def get_sources():

    try:
        es = get_connection()
    except:
        return {
            "error" : "cant connect to elasticsearch"
        }
    
    index_name = "sources"

    query = {
            "match_all": {}
        }

    sort = [
            {
                "name.keyword": {
                    "order": "asc"
                }
            }
        ]

    response = es.search(index=index_name, query=query, sort=sort)
    hits = response['hits']['hits']

    sources = []
    for hit in hits:
        source = {
            'id' : hit['_id'],
            **hit['_source']
        }
        sources.append(source)
    
    return sources 


@app.post("/markasread")
def markasread(query: PostQuery):
    try:
        es = get_connection()
    except:
        return {
            "error" : True,
            "message" : "cant connect to elasticsearch",
        }

    response = es.update(index="articles", id=query.post_id, doc={"read": True})
    
    return {
        "message" : "marked as read",
    }

@app.post("/posts")
def get_posts(query: PostsQuery):

    try:
        es = get_connection()
    except:
        return {
            "error" : True,
            "message" : "cant connect to elasticsearch",
        }


    # range query 
    range_query = None
    if query.start_date is not None:
        range_query = {
            "range": {
                "date_time": {
                    "gte": query.start_date,
                }
            }
        }
    
    if query.end_date is not None:
        if range_query is None:
            range_query = {
                "range": {
                    "date_time": {
                        "lte": query.end_date,
                    }
                }
            }
        else:
            range_query['range']['date_time']['lte'] = query.end_date


    # source query 
    source_query = None
    
    if query.sources is not None and len(query.sources) > 0:
        source_query = {
            "terms": {
                "source_id.keyword": query.sources
            }
        }
    
    # search query
    search_query = None
    search_highlight = None
    if query.search is not None:
        search_query = {
            "multi_match": {
            "query": query.search,
            "fields": ["title", "content"]
            }
        }
        search_highlight = {
            "pre_tags": ["<b>"],
            "post_tags": ["</b>"],
            "fields": {
                "title": {"number_of_fragments": 0},
                "content": {"number_of_fragments": 0}
            }
        }
    # combine all queries
    
    

    if range_query is None and source_query is None and search_query is None:
        combined_query = {
            "match_all": {}
        }
    else:
        combined_query = {
            "bool": {}
        }
        if 'must' not in combined_query['bool']:
            combined_query['bool']['must'] = []

        if range_query is not None:
            combined_query['bool']['must'].append(range_query)
        if source_query is not None:
            combined_query['bool']['must'].append(source_query)
        if search_query is not None:
            combined_query['bool']['must'].append(search_query)
            
    # sort query
    sort = []
    if query.sort == 'By date':
        sort = [
            {
                "date_time": {
                    "order": "desc"
                }
            }
        ]
    elif query.sort == 'By title':
        sort = [
            {
                "title.keyword": {
                    "order": "asc"
                }
            }
        ]
    elif query.sort == 'By relevance':
        sort = [
            {
                "_score": {
                    "order": "desc"
                }
            }
        ]
    else:
        sort = [
            {
                "date_time": {
                    "order": "desc"
                }
            }
        ]
        
    
    # size and page
    size = query.size
    page = query.page * size

    
    response = es.search(index="articles", query=combined_query, highlight = search_highlight , sort = sort, from_ = page, size=size)
    total = response['hits']['total']['value']
    hits = response['hits']['hits']
    data = []
    for hit in hits:
        article = hit['_source']
        article['id'] = hit['_id']
        if 'highlight' in hit:
            if 'title' in hit['highlight']:
                article['title'] = hit['highlight']['title'][0]
            if 'content' in hit['highlight']:
                article['content'] = hit['highlight']['content'][0]

        data.append(article)


    return {
        "data" : data,
        "total" : total,
        "per_page" : size
    }

    
