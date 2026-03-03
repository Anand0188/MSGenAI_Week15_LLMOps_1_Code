
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration for Wanderlust Travel Chatbot"""

    # ====================
    # Azure OpenAI Configuration
    # ====================
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5-mini")
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv(
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small"
    )

    # ====================
    # Azure AI Search Configuration (Only vector store - no ChromaDB)
    # ====================
    AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
    AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
    AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME", "travel-kb-index")

    # ====================
    # Azure Storage (Optional)
    # ====================
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    AZURE_STORAGE_CONTAINER_NAME = os.getenv(
        "AZURE_STORAGE_CONTAINER_NAME", "travel-documents"
    )

    # ====================
    # Azure Content Safety (Optional)
    # ====================
    AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    # ====================
    # Azure Monitor (Optional)
    # ====================
    APPLICATIONINSIGHTS_CONNECTION_STRING = os.getenv(
        "APPLICATIONINSIGHTS_CONNECTION_STRING"
    )

    # ====================
    # MLflow Configuration
    # ====================
    MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
    MLFLOW_EXPERIMENT_NAME = os.getenv(
        "MLFLOW_EXPERIMENT_NAME", "wanderlust-travel-chatbot"
    )

    # ====================
    # Ingestion Settings
    # ====================
    INGESTION_LIMIT = int(os.getenv("INGESTION_LIMIT", "0"))
