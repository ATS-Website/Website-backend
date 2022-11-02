from algoliasearch_django import algolia_engine


def get_client():
    return algolia_engine.client


def get_index(index_name="cfe_Blog"):
    client = get_client()
    index = client.init_index(index_name)
    return index


def perform_search(query, **kwargs):
    """perform_search("hello",tags=["Estate"],public=True)"""
    index = get_client()
    params = {}
    tags = ''
    if tags in kwargs:
        tags = kwargs.pop("tags") or []
        if len(tags) != 0:
            params["tagFilters"] = tags
    index_filters = [f"{k}:{v}" for k, v in kwargs.items() if v]
    if len(index_filters) != 0:
        params["facetFilters"] = index_filters
    results = index.search(query, params)
    return results
