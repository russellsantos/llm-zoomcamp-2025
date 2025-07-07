# Overview

This contains my notes for the dlt-workshop module of the LLM Zoomcamp.

[Link to Module](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2025/workshops/dlt.md)



This is not super organized, this will just contain things I think I need to remember from the course.



# Video: From Rest to reasoning 
[Source](https://www.youtube.com/watch?v=MNt_KK32gys)
[Slides](https://docs.google.com/presentation/d/1oHQilxEVqGGW4S2ctNEE0wHY2LgcjYLaRUziAoinsis/edit?usp=sharing)
[Collab Notebook](https://colab.research.google.com/drive/1vBA9OIGChcKjjg8r5hHduR0v3A5D6rmH?usp=sharing)

 - We'll be using [dlt](https://dlthub.com/docs/intro). Essentially a library that helps with loading data from various sources.
 - [Cognee](https://www.cognee.ai/) will also be used. it's a library for AI memory. 

 ## DLT
  - open source for building piplines usingi just python code. 
  - extracts data fro mapis, databases, etc
  - transform and normalize data
  - load data into destinations like bigwquery ,duckdb, redshift.

## Cognee 
  - GraphRag - using a knowledge graph to store data instead of vector database
  - Cognee can automatically build a knowledge graph from structured or unstructured data
  - ask natural language questions 
  - stores datapoints, and relationships between datapoints.
  - supposedly cognee also enriches the data? Not sure what this looks like. 
  - stores enriched data to cognee memory. Not really sure what this looks like as well. 
  - Graph retrieval can supposedly help with quality and relevance of context, because it would be a semantic search.
  - part of rag challenges is also ranking and consolidation, becaues cosine simialrity might not be useful for ranking, and graph traversal can help with prioritization of releavant data.
  - another challenge is pipeline scalability - ingestion can be resource intensive. Cognee can help with this by reducing complexity in ETL 

## Cognee Node Sets
 - tags that you add to different content in the knowledge graphs 
 - can be use dfor filtering using topics 
 - can make it easier to analyze patterns per topic. 
 - graph dtabases used with Cognee need to support node sets. Kuzu and Neo4j

 ## On the Notebook
 [Collab Notebook](https://colab.research.google.com/drive/1vBA9OIGChcKjjg8r5hHduR0v3A5D6rmH?usp=sharing#scrollTo=RRtqeThCjfsc)
  - when not specifying a graph db, will use NetworkX by default.
  - in hte notebook, partitioning is manual, but DLT can support partitioning. [Docs here](https://dlthub.com/docs/plus/ecosystem/iceberg#partitioning)
  - when adding data, `cognee.add` is best for text data. You may need to use relational data otherwise.
## Demo 2
 - building RAGs for understanding docs. 
 - we will want to use ontology. Ontology is useful as 
  - provides shared vocabulary
  - structures the data
  - allow reasoning using the data
  - supports interoperability of different data sources.
  - [filesystem_pipeline.py](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2025/workshops/dlt/filesystem_pipeline.py) - reads data from the downloaded docs for specific sites, and converts it to a csv with fields `source_name`, `node_set_category`, `filename` and `content`.
  - [mount_cognee.py](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2025/workshops/dlt/mount_cognee.py) loads the csv file and adds this to cognee. Note that it first loads all the data via `cognee.add()` then `cognee.cognify()`. Then afterwards, it adds the ontology through `cognree.cognify(ontology_file_path='<ontology-path>')`
  - note: the ontology file was created by Chatgpt, apparently, by describing what is available.
  - once data is added, call `cognee.search()`. can use `node_set` parameter to filter depending on node sets.

# Homework 

## Q1 DLT version
Note: i'll be using pipenv here as well. We'll run these commands insdie the `dlt-workshop` folder.

```bash 
$ pipenv --python 3.12
$ pipenv install "dlt[qdrant]" "qdrant-client[fastembed]"
```
Then we see what's the version of dlt used:
```bash
$ pipenv run pip list | grep dlt
``` 
### DLT Resource
  - created `dlt_pipelin.py` for this puprose. 
  - used `max_table_nesting=0` to ensure we only have one table, as it makes sense for our FAQ data.

## Q2 dlt pipeline.
 - run `pipenv run python ./dlt_pipeline.py`