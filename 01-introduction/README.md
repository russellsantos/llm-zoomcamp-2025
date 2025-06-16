# LLM Zoomcamp - Module 1: Introduction

This directory contains the setup and scripts for the first module of the LLM Zoomcamp course.

## Prerequisites

- Docker and Docker Compose
- Python 3.13+
- pipenv

## Setup

### 1. Elasticsearch

The `docker-compose.yml` file contains the configuration for Elasticsearch 8.17.6:

```bash
# Start Elasticsearch
docker-compose up -d

# Check if it's running
curl localhost:9200

# Stop Elasticsearch
docker-compose down
```

### 2. Python Environment

A Python virtual environment is set up using pipenv:

```bash
# Install dependencies
pipenv install

# Activate the environment
pipenv shell

# Or run commands directly
pipenv run python script.py
```

### 3. FAQ Data

Download the FAQ data used in the course:

```bash
# Download FAQ data
pipenv run python download_faq_data.py

# Examine the downloaded data
pipenv run python examine_data.py
```

## Files

- `docker-compose.yml` - Elasticsearch configuration
- `Pipfile` - Python dependencies
- `download_faq_data.py` - Script to download FAQ data
- `examine_data.py` - Script to examine the downloaded data
- `documents.json` - Downloaded FAQ data (created after running download script)

## FAQ Data Structure

The downloaded data contains:
- **948 total documents** from 3 courses:
  - data-engineering-zoomcamp: 435 documents
  - machine-learning-zoomcamp: 375 documents
  - mlops-zoomcamp: 138 documents

Each document has the following structure:
- `text`: The content/answer
- `section`: The section it belongs to
- `question`: The question being answered
- `course`: The course it belongs to

## Next Steps

With Elasticsearch running and the FAQ data downloaded, you're ready to proceed with the course exercises for indexing and searching the documents.
