from algoliasearch.search_client import SearchClient
from algoliasearch_django import algolia_engine
from .models import BlogArticle


def get_client():
    return algolia_engine.client


def get_index(index_name="ats_BlogArticle"):
    client = get_client()
    index = client.init_index(index_name)
    return index


# # hello_algolia.py

# # Connect and authenticate with your Algolia app
# client = SearchClient.create("KS8I4QDCP2", "YourWriteAPIKey")
# def perform_search(query, **kwargs):
#     """perform_search("hello",tags=["Estate"],public=True)"""
#     index = get_client()
#     params = {}
#     tags = ''
#     print("Here")
#     if tags in kwargs:
#         tags = kwargs.pop("tags") or []
#         if len(tags) != 0:
#             params["tagFilters"] = tags
#     index_filters = [f"{k}:{v}" for k, v in kwargs.items() if v]
#     if len(index_filters) != 0:
#         params["facetFilters"] = index_filters
#     print(index.create())
#     results = index.search(query)
#     return results
