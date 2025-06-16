#!/usr/bin/env python3

import json
from elasticsearch import Elasticsearch
from tqdm import tqdm


def create_elasticsearch_client(host='localhost', port=9200):
    es = Elasticsearch(
        [f'http://{host}:{port}'],
        verify_certs=False,
        ssl_show_warn=False
    )
    
    if es.ping():
        print(f"Connected to Elasticsearch at {host}:{port}")
        info = es.info()
        print(f"   Elasticsearch version: {info['version']['number']}")
        return es
    else:
        raise RuntimeError(f"Could not ping Elasticsearch at {host}:{port}")
    
def create_index(es, index_name='course-questions'):
    if es.indices.exists(index=index_name):
        print(f"Index '{index_name}' already exists. Deleting...")
        es.indices.delete(index=index_name)
    
    es.indices.create(index=index_name)
    print(f"Created index '{index_name}'")
    return True


def load_documents(file_path='documents.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        documents = json.load(f)
    
    print(f"Loaded {len(documents)} documents from {file_path}")
    return documents
        

def index_documents(es, documents, index_name='course-questions'):
    print(f"Indexing {len(documents)} documents...")
    
    success_count = 0
    error_count = 0
    
    for i, doc in enumerate(tqdm(documents, desc="Indexing documents")):
        response = es.index(
            index=index_name,
            id=i,
            body=doc
        )
        success_count += 1
    
    print(f"Indexing complete!")
    print(f"Successfully indexed: {success_count} documents")
    if error_count > 0:
        print(f"Errors: {error_count} documents")
    
    es.indices.refresh(index=index_name)
    print(f"Index '{index_name}' refreshed")
    
    
def main(documents_file='documents.json', index_name='course-questions', 
         es_host='localhost', es_port=9200):
    print("Starting document indexing process...\n")
    
    es = create_elasticsearch_client(es_host, es_port)
    
    documents = load_documents(documents_file)
    
    create_index(es, index_name)
    
    index_documents(es, documents, index_name)
    
    
    print(f"\nSuccessfully indexed documents into Elasticsearch!")
    return True


if __name__ == "__main__":
    main()
