# Overview

This serves as my notes for module 02 of the LLM Zoomcamp. These notes will be a bit disjointed, as I am nothing things down as I go through the course. 


# Videos

## 2.1 Getting Started with Vector Search and Qdrant
### How it works
 - we store vector representations of words into the vector database.
 - dedicated vector databases are necessary because it can scale in production, and can go beyond similarity search.

### Setup 
 - will use the `qdrant/qdrant` docker image. 
 - `docker run qdarnt/qdrant -p 6333:6333 6334:6334 -v"{$pwd}/qdrant_storage:/qdrant/storage` to launch qdrant. 
 - i've created a docker-compose file to make it easier to set this up in the future.
 - we can access the Qdrant UI dashboard on `http://localhost:6333/dashboard`
 - port 6333 also contains an API to access the server
 - alternativeely port 6334 is forr gRPC


### Required Libraries 
 - Note: i'll be using pipenv here too.
 - qdrant-client package `python -m install -q "qdrant-client[fastembed]>=1.14.2"`
## 2.2 Studying the dataset & Choosing an Embedding Model with FastEmbed
Video: https://www.youtube.com/watch?v=4lX6sbdrs84&list=PL3MmuxUbc_hIB4fSqLy_0AfTjVLpgjV3R&index=10 
 -  out data now comes chunked for now 
 - we will need to specify what fields can be used for semantic search, and what fields used as metadata.
 - for this example, since we're building a Q&A RAG system, it makes sens to store the answers as embeddings, and then, when retrieving context, convert question to embedding.
 - course and section can be used as metadata, since we can use those for filtering.
 - choice of embedding model depends on
    - the task , type of data (data modality) and other specifics
    - tradeoff between precision and resource usage (bigger embeddings need more resources)
    - cost of inference ? 
 - we will need to test and benchmark.
 - for embeddings, using FastEmbed makes sense, because it's optimized (already quantize, etc).
 - for this purpose - we need English embeddings, and we don't need multi-modal models, since we are only using text data, so `jina-embedding-smal-en` is good choice.
 - most embedding models use `cosine similarity` when trying to measure closeness.
 - FastEmbed can be run on GPU's to make it faster.
 - also supports batch_upsert
 - embedding with fastEmbedd happens LOCALLY, so if we are going to consider GPU, that happens where the client is running. 
  - when searching ,need to convert query to vector using models.Document. Will need to use the exact same embedding model.
  - `client.query_points` has parameters like `with_payload` to include metadata, and `limit` in order to get top n matches.
  - if we want to use metadata for filters, you will need to create a payload index using `client.create_payload_index`, and  then ues `query_filter` parameter in the `client.query_points` method.