import dlt 
import requests
from dlt.destinations import qdrant

@dlt.resource(table_name='zoomcamp_data', max_table_nesting=0)
def zoomcamp_data():
    docs_url = 'https://github.com/alexeygrigorev/llm-rag-workshop/raw/main/notebooks/documents.json'
    docs_response = requests.get(docs_url)
    documents_raw = docs_response.json()

    for course in documents_raw:
        course_name = course['course']

        for doc in course['documents']:
            doc['course'] = course_name
            yield doc



def main():
    qdrant_destination = qdrant(
        qd_path="db.qdrant",
    )
    pipeline = dlt.pipeline(
        pipeline_name="zoomcamp_pipeline",
        destination=qdrant_destination,
        dataset_name="zoomcamp_tagged_data",
    )
    load_info = pipeline.run(zoomcamp_data)
    print(pipeline.last_trace)

if __name__ == "__main__":
    main()


