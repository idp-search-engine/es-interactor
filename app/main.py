from fastapi import FastAPI
from elasticsearch import AsyncElasticsearch
from pydantic import BaseModel
import os

es_host = os.environ['ES_HOST']
es_user = os.environ['ES_USER']
es_password = os.environ['ES_PASSWORD']
es_index = os.environ['ES_INDEX']
es_index_pipeline = os.environ['ES_INDEX_PIPELINE']

app = FastAPI()
es = AsyncElasticsearch(es_host,
                        basic_auth=(es_user, es_password),
                        verify_certs=False)

class EsPageBody(BaseModel):
    original_url: str
    text: str


def get_es_query(query: str):
    print(query)
    return {
            "simple_query_string": {
                "query": query,
                "fields": ["text", "url"]
            }
        }


@app.on_event("shutdown")
async def app_shutdown():
    await es.close()


@app.get('/query')
async def query(q: str):
    results = await es.search(index=es_index,
                              query=get_es_query(q))
    return results


@app.post('/pages/add')
async def add_page(body: EsPageBody):
    resp = await es.index(index=es_index,
                          document=body.dict(),
                          pipeline=es_index_pipeline)
    return {"id": resp["_id"]}
