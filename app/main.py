from fastapi import FastAPI
from elasticsearch import AsyncElasticsearch
from pydantic import BaseModel
import os

user = os.environ['ES_USER']
password = os.environ['ES_PASSWORD']

app = FastAPI()
es = AsyncElasticsearch('https://127.0.0.1:9200',
                        basic_auth=(user, password),
                        verify_certs=False)


class EsSimpleQueryRequestBody(BaseModel):
    query: str


def get_es_query(query: str):
    return {
            "simple_query_string": {
                "query": query,
                "fields": ["site_text", "url"]
            }
        }


@app.on_event("shutdown")
async def app_shutdown():
    await es.close()


@app.get('/')
async def root(body: EsSimpleQueryRequestBody):
    results = await es.search(index='websites',
                              query=get_es_query(body.query))
    return results
