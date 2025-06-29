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

 ## 2.5 RAG with Vector Search
 - essently, we can do search on the vector database, then put results into the prompt before we send to llm.


 ## 2.6 Hybrid Search with Qdrant
 - keyword search is implemented as vector search, but generally speaking is sparse vectors
  - essentialy, dimensions of the vector represent words, and the vector will contain 1 if text has that word, adn 0 if not. Therefore there will be a lot of 0's and 1's.
  - can still be uesful in many cases. 
  - may be able to cover texts that would look like random characters for dense vectors , for eg, proper names. We can add "new" words at the end.
  - BM25(best matching 25) is a standard ranking for sparse embeddings. this makes use of Term Frequency (FT) and Inverse Document Frequency (IDF). This is also in FastEmbed?
  - QDrant can use Sparse Vectors to store collections. We can also cofnigure it to use BM25 by using the models.Modifier.IDF
  - when upserting, we need to provide the model "Qdrant/bm25" to use the appropriate conversion.
  - upserting is pretty fast, since there is no neural network used.
  - sparse vectors can return no results if no matches in keywords.
  - it doesn't work so well with semantic queries tho.
  - Qdrant supports hybrid - having multi-step search piplines and reranking.
  - to do hybrid, you'll need to create a collection that supports both dense and sparse vectors (use vectors_cofnig, and sparse_vectors_config when creating collection)
  - based on how this is structured, we might also be able to use multiple types of embeddings in the same collection?
  - when querying, use `prefetch` get an initial set of results, then this will be passed to the normal query.
  - alternatively, one can use a re-ranking function to do hybrid search. Here', we can use multiple different methods in the `prefectch` and use a reranking function in the query to combine things. An example here is the Fusion query.
  - alternatively one can use cross-encoders or multivecto representations. This is something we can look into in the future.
