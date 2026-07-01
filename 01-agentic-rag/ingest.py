"""
Data ingestion module for the RAG system.

This module handles fetching the FAQ dataset from the DataTalks.club API
and building a searchable index. It is designed to be imported by notebooks
and the rag_helper module.

Functions:
    load_faq_data: Fetch all course FAQ documents from the remote API.
    build_index: Create a minsearch index from the loaded documents.
"""

import requests
from minsearch import Index


def load_faq_data():
    """
    Fetch the complete FAQ corpus from DataTalks.club.

    Returns:
        list[dict]: A flat list of FAQ documents. Each document contains
        at least the keys: id, course, section, question, answer.

    Raises:
        requests.HTTPError: If any course FAQ endpoint returns a bad status.
    """
    docs_url = "https://datatalks.club/faq/json/courses.json"
    response = requests.get(docs_url)
    courses_raw = response.json()

    documents = []
    url_prefix = "https://datatalks.club/faq"

    for course in courses_raw:
        course_url = f"""{url_prefix}{course["path"]}"""
        course_response = requests.get(course_url)
        course_response.raise_for_status()
        course_data = course_response.json()

        documents.extend(course_data)

    return documents


def build_index(documents):
    """
    Build a minsearch search index from a list of documents.

    The schema defines which fields are tokenized/scored (text_fields)
    and which are used for exact filtering (keyword_fields).

    Args:
        documents (list[dict]): List of FAQ documents with string fields.

    Returns:
        minsearch.Index: A fitted search index ready for .search() calls.
    """
    index = Index(
        text_fields=["question", "section", "answer"],
        keyword_fields=["course"]
    )
    index.fit(documents)
    return index