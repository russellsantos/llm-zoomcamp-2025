#!/usr/bin/env python3

import json
from elasticsearch import Elasticsearch


def create_elasticsearch_client(host='localhost', port=9200):
    es = Elasticsearch(
        [f'http://{host}:{port}'],
        verify_certs=False,
        ssl_show_warn=False
    )
    
    if es.ping():
        print(f"Connected to Elasticsearch at {host}:{port}")
        return es
    else:
        raise RuntimeError(f"Could not ping Elasticsearch at {host}:{port}")


def search_documents_filtered(es, query_text, course_filter, index_name='course-questions'):
    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": query_text,
                            "fields": ["question^4", "text"],
                            "type": "best_fields"
                        }
                    },
                    {
                        "match_phrase": {
                            "course": course_filter
                        }
                    }
                ]
            }
        }
    }
    
    response = es.search(index=index_name, **search_query)
    return response


def display_results(response):
    print(f"Found {response['hits']['total']['value']} total results")
    print(f"Showing top {len(response['hits']['hits'])} results:\n")
    
    for i, hit in enumerate(response['hits']['hits'], 1):
        source = hit['_source']
        score = hit['_score']
        
        print(f"Result {i} (Score: {score:.2f})")
        print(f"Course: {source.get('course', 'N/A')}")
        print(f"Section: {source.get('section', 'N/A')}")
        print(f"Question: {source.get('question', 'N/A')}")
        print(f"Answer: {source.get('text', 'N/A')[:200]}...")
        print("-" * 80)


def main():
    query_text = "How do copy a file to a Docker container?"
    course_filter = "machine-learning-zoomcamp"
    
    print(f"Executing query: '{query_text}'")
    print(f"Filtering by course: '{course_filter}'")
    print("=" * 80)
    
    es = create_elasticsearch_client()
    response = search_documents_filtered(es, query_text, course_filter)
    display_results(response)


if __name__ == "__main__":
    main()
