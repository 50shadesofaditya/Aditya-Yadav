from elasticsearch import Elasticsearch

def fetch_logs_from_elk(host="localhost", port=9200, index="logs-*", minutes=5):
    es = Elasticsearch(f"http://{host}:{port}")
    body = {"query": {"range": {"@timestamp": {"gte": f"now-{minutes}m", "lte": "now"}}}}
    res = es.search(index=index, size=1000, body=body)
    return [h['_source'] for h in res['hits']['hits']]
