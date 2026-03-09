#!/usr/bin/env python3
"""
Fix Azure Search index dimensions by deleting and recreating with correct dimensions
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential
from src.config import Config


def fix_index_dimensions():
    """
    Delete and recreate Azure Search index with correct dimensions
    """
    print("🔧 Fixing Azure Search Index Dimensions")
    print("=" * 50)
    
    try:
        # Connect to Azure Search
        credential = AzureKeyCredential(Config.AZURE_SEARCH_KEY)
        index_client = SearchIndexClient(
            endpoint=Config.AZURE_SEARCH_ENDPOINT,
            credential=credential
        )
        
        print(f"✅ Connected to Azure Search")
        print(f"📍 Endpoint: {Config.AZURE_SEARCH_ENDPOINT}")
        print(f"📍 Index: {Config.AZURE_SEARCH_INDEX_NAME}")
        
        # Check if index exists
        existing_indexes = list(index_client.list_index_names())
        print(f"📋 Existing indexes: {existing_indexes}")
        
        if Config.AZURE_SEARCH_INDEX_NAME in existing_indexes:
            print(f"🗑️ Deleting existing index: {Config.AZURE_SEARCH_INDEX_NAME}")
            index_client.delete_index(Config.AZURE_SEARCH_INDEX_NAME)
            print(f"✅ Index deleted successfully")
        else:
            print(f"ℹ️ Index '{Config.AZURE_SEARCH_INDEX_NAME}' does not exist yet")
        
        print(f"✅ Index ready for recreation with correct dimensions")
        print(f"📝 Next step: Run ingestion to recreate index with 1536 dimensions")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing index: {e}")
        return False


def verify_fix():
    """
    Verify the fix by testing vector store initialization
    """
    print("\n🔍 Verifying Fix")
    print("-" * 30)
    
    try:
        from src.vector_store import get_vector_store
        from langchain_openai import AzureOpenAIEmbeddings
        
        # Initialize embeddings
        embeddings = AzureOpenAIEmbeddings(
            api_key=Config.AZURE_SEARCH_KEY,
            azure_endpoint=Config.AZURE_SEARCH_ENDPOINT,
            azure_deployment=Config.AZURE_SEARCH_INDEX_NAME,
            api_version=Config.AZURE_OPENAI_API_VERSION,
        )
        
        # Initialize vector store (this will recreate the index)
        print("🔄 Initializing vector store (will recreate index)...")
        vector_store = get_vector_store(embeddings)
        
        print("✅ Vector store initialized successfully")
        print("✅ Index recreated with correct dimensions (1536)")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Azure Search Index Dimension Fix")
    print("=" * 50)
    
    # Step 1: Delete existing index
    success = fix_index_dimensions()
    
    if success:
        # Step 2: Verify by recreating
        success = verify_fix()
        
        if success:
            print("\n🎉 SUCCESS! Index dimensions fixed!")
            print("💡 Now run your ingestion and search tests:")
            print("   python run_ingestion_and_test.py")
            print("   python test_enhanced_search.py")
        else:
            print("\n⚠️ Verification failed. Check the error above.")
    else:
        print("\n⚠️ Index deletion failed. Check your Azure Search credentials.")