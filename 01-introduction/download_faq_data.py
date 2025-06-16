#!/usr/bin/env python3

import requests
import json


def download_and_process_documents():
    print("Downloading FAQ data...")
    
    # URL for the documents JSON file
    docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'
    
    docs_response = requests.get(docs_url)
    docs_response.raise_for_status()  
    documents_raw = docs_response.json()
    
    print(f"Downloaded data for {len(documents_raw)} courses")
    
    documents = []
    
    for course in documents_raw:
        course_name = course['course']
        print(f"Processing course: {course_name}")
        
        for doc in course['documents']:
            doc['course'] = course_name
            documents.append(doc)
    
    print(f"Total documents processed: {len(documents)}")
    
    return documents
    


def write_documents_to_file(documents, output_file='documents.json'):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)
    
    print(f"Documents saved to {output_file}")
    return True


def main():
    documents = download_and_process_documents()
    write_documents_to_file(documents)


if __name__ == "__main__":
    documents = main()
