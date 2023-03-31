from fastapi import FastAPI
from elasticsearch import AsyncElasticsearch
from pydantic import BaseModel

app = FastAPI()
es = AsyncElasticsearch('https://127.0.0.1:9200',
                        basic_auth=('elastic', 'morbius'),
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


@app.get('/')
async def root(body: EsSimpleQueryRequestBody):
    results = await es.search(index='websites',
                              query=get_es_query(body.query))
    print(results)
    return {'Message': 'Hello world!'}
