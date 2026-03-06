from src.config import Config
from langchain_community.vectorstores import AzureSearch

from azure.search.documents.indexes.models import (
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile
)


def get_vector_store(embedding_function):

    endpoint = Config.AZURE_SEARCH_ENDPOINT
    key = Config.AZURE_SEARCH_KEY
    index_name = Config.AZURE_SEARCH_INDEX_NAME

    if not endpoint or not key:
        raise ValueError("AZURE_SEARCH_ENDPOINT and AZURE_SEARCH_KEY must be set.")

    # Azure Search Index Fields
    fields = [
        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True
        ),

        SearchableField(
            name="content",
            type=SearchFieldDataType.String
        ),

        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            vector_search_dimensions=1536,
            vector_search_profile_name="vector-profile"
        ),

        SearchableField(
            name="metadata",
            type=SearchFieldDataType.String
        )
    ]

    # Vector Search Configuration
    vector_search = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(
                name="hnsw-config"
            )
        ],
        profiles=[
            VectorSearchProfile(
                name="vector-profile",
                algorithm_configuration_name="hnsw-config"
            )
        ]
    )

    vector_store = AzureSearch(
        azure_search_endpoint=endpoint,
        azure_search_key=key,
        index_name=index_name,
        embedding_function=embedding_function.embed_query,
        fields=fields,
        vector_search=vector_search,
        content_key="content",
        vector_key="content_vector",
        metadata_key="metadata"
    )

    print(f"✅ Initialized Azure AI Search index '{index_name}'")

    return vector_store