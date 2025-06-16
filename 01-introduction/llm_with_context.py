#!/usr/bin/env python3

import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from elasticsearch import Elasticsearch
import tiktoken

load_dotenv(find_dotenv())


def query_openai(question, context, model="gpt-3.5-turbo"):
    client = OpenAI()
    prompt_template = """
    You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
    Use only the facts from the CONTEXT when answering the QUESTION.

    QUESTION: {question}

    CONTEXT:
    {context}
    """.strip()
    
    prompt = prompt_template.format(context=context, question=question)
    
    token_count = count_tokens(prompt, model)
    print(f"Prompt tokens: {token_count}")
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    
    return response.choices[0].message.content


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
        "size": 3,
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


def build_context(search_results):
    context_parts = []
    context_template = """
    Q: {question}
    A: {text}
    """.strip()
   
    for hit in search_results['hits']['hits']:
        doc = hit['_source']
        context_parts.append(
            context_template.format(
                question=doc.get('question', ''),
                text=doc.get('text', '')
            )
        )
    
    return "\n\n".join(context_parts)


def get_context_from_elasticsearch(question, course_filter="machine-learning-zoomcamp"):
    es = create_elasticsearch_client()
    search_results = search_documents_filtered(es, question, course_filter)
    context = build_context(search_results)
    return context


def count_tokens(text, model="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)


def main():
    question = "How do I copy files from my local machine to docker container?"
    
    print(f"Question: {question}")
    
    print("Getting context from Elasticsearch...")
    context = get_context_from_elasticsearch(question)
    
    print(f"Context retrieved ({len(context)} characters)")
    
    answer = query_openai(question, context, model='gpt-4o')
    print(f"Answer: {answer}")


if __name__ == "__main__":
    main()


