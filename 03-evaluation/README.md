# 03 - Evaluation

This doc will contain my notes for the 3rd module of the LLM Zoomcamp - Evaluation. 

# Video Notes


## 3.0 Content update explanation video

 - nothing much here of note except for :
    - we will be using the `search_evaluation_folder` and the `rag_evaluation_folder` in the module
    - We'll also be making use of minsearch instead of elasticsearch.
    - we'll need the sentence transformers library.

- As with the others, we'll be creating a different pip environment for this module. We'll run the following:
    ```bash
    $ pipenv --python 3
    $ pipenv install ipykernel jupyter minsearch openai pickle
    $ pipenv install sentence-transformers #as we will be using this through the module
    ```

## 3.1 - Evaluation Metrics for Retrieval

    - what's the best metric? IT DEPENDS.  
    - you should have ground truth data for each query
        -eg. Query: I just discovered the course. Can I still join? 
        -       Relevant documents: doc1, doc10, doc11? 
        - you should use different metrics based on what makes sense for your ground truth.
    - ideally you should use feedback from users as ground truth, but since we don't have production yet, we can generate the ground truth.
    - common ranking evaluation metircs
        - Precision at k (P@K) - Number of relevant documents in top k results / k 
        - Recall
            - measures the number of relevant documents retrieve out of the total number of relevant documents available.
        - Hit Rate (or recall at k) - will be used in module
        - Mean reciprocal Rank - will be used in module.
## 3.2 - Ground truth Dataset Generation for Retrieval Evaluation

    - typically for each query you have multiple relevant docs, but for now, we'll assume 1.
    - how to generate?
        for each record in FAQ, we generate 5 questions. The "record" is the relevant document.
    - we'll be using an llm to generate. in real life, we may use human annotattors. An alterative is looking through common questions asked by customers.
    - ideally we will need a unique id to represent the questions. if there is no such identifier in the data, we can create one by hashing some combination of the content (course, chapter, question). Just make sure that there are no id collisions.
    - sometimes the json that the AI returns isn't valid. You may need to alter it yourself.