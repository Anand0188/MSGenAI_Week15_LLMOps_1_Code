"""
Streamlit UI Application
RUBRIC: Streamlit UI Application (6 marks total)
- Page config and layout implemented (2 marks)
- Search integrated correctly (2 marks)
- Results and sources displayed (1 mark)
- UI/UX design and examples (1 mark)

TASK: Create Streamlit web interface for travel chatbot
"""
import sys
import os
import traceback
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.search_engine import TravelSearchEngine
from src.config import Config
import src.monitoring  # Enable MLflow/Azure Monitor
import time

# HINT: Set page config with title and layout
st.set_page_config(page_title="WanderNest Travels - AI Assistant", layout="wide")  # HINT: "WanderNest Travels - AI Assistant", "wide"

st.title("WanderNest Travels - AI Assistant")  
st.markdown("Get instant answers about flights, hotels, policies, and travel requirements.")  # HINT: "Get instant answers about flights, hotels, policies, and travel requirements."

# ====================
# Initialize Engine
# ====================
@st.cache_resource
def get_engine():
    """
    Initialize and cache the search engine
    
    HINT: Try to return TravelSearchEngine(), handle exceptions
    """
    try:
        return TravelSearchEngine() 
    except Exception as e:
        st.error(f"Failed to initialize search engine: {e}")
        st.error("Please check the configuration and try again.")
        return None

def display_results(results, query_text, generated_response):
    """
    Display search results and AI response
    
    HINT: This function should:
    1. Show success message with result count
    2. Display AI Response in container
    3. Show source documents in expander
    """
    st.success(f"Found {len(results)} relevant documents.")  
    
    # HINT: Show AI Response
    st.subheader("AI Response")  
    with st.container():
        st.markdown(generated_response)  
    
    # HINT: Show Sources
    if results:
        with st.expander("View Source Documents"):  # HINT: "View Source Documents"
            for i, doc in enumerate(results):
                with st.container():
                    st.markdown(f"**{i+1}. Source: {doc.metadata.get('source', 'Unknown')}**") 
                    st.markdown(f"*Category: {doc.metadata.get('category', 'N/A')}*")  
                    st.write(doc.page_content[:400] + "...")  # HINT: page_content
                    st.divider()
    else:
        st.warning("No relevant documents found.")

# HINT: Get engine instance (deferred initialization for faster loading)
engine = None

# HINT: Cache clear option (for debugging)
if st.sidebar.button("Clear Cache"): 
    st.cache_resource.clear()
    st.rerun()

# ====================
# Sidebar
# ====================
with st.sidebar:
    st.header("About") 
    st.info("""
    **WanderNest Travels AI Assistant**
    
    This chatbot helps you with:
    - Flight policies & routes
    - Baggage rules
    - Visa requirements  
    - Hotel information
    - Booking & cancellation policies
    
    Powered by Azure AI & RAG
    """)
    
    st.divider()
    
    st.header("Statistics")  # HINT: "Statistics"
    if 'query_count' not in st.session_state:
        st.session_state.query_count = 0  
    st.metric("Total Queries", st.session_state.query_count)

# ====================
# Main Search Interface
# ====================
st.markdown("### ___")  # HINT: "🔍 Ask Your Travel Questions"

# HINT: Example questions in 3 columns
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Baggage Rules"):  # HINT: "Baggage Rules"
        st.session_state.example_query = "What are the baggage allowance rules for international flights?"  # HINT: "What are the baggage allowance rules for international flights?"
with col2:
    if st.button("Visa Info"):  # HINT: "Visa Info"
        st.session_state.example_query = "Do I need a visa to travel from India to UK?"  # HINT: "Do I need a visa to travel from India to UK?"
with col3:
    if st.button("Cancellation Policy"):  # HINT: "Cancellation Policy"
        st.session_state.example_query = "What is the cancellation policy for Air India flights?"  # HINT: "What is the cancellation policy for Air India flights?"

st.divider()

# HINT: Get query (from example or text input)
if 'example_query' in st.session_state:
    query_text = st.session_state.example_query
    del st.session_state.example_query
else:
    query_text = st.text_input(
        "Enter your travel question",
        placeholder="e.g., 'What are the baggage rules for BLR to LON?'",  # HINT: "e.g., 'What are the baggage rules for BLR to LON?'"
        label_visibility="collapsed"
    )

search_button = st.button("Search", use_container_width=True, type="primary")  # HINT: "Search"

# ====================
# Search Logic
# ====================
if search_button and query_text:
    # Initialize engine on first use for faster page load
    if engine is None:
        with st.spinner("Initializing search engine..."):
            engine = get_engine()
    
    if engine is None:
        st.error("Failed to initialize search engine. Please check the configuration.")
    else:
        st.session_state.query_count += 1  
        
        st.markdown("---")
        with st.spinner("Searching travel knowledge base..."):  # HINT: "Searching travel knowledge base..."
            start_time = time.time()
            
            try:
                # HINT: Search for relevant documents
                results, processed_query = engine.search_by_text(query_text, k=5) 
                
                # HINT: Generate AI response
                generated_response = engine.synthesize_response(results, query_text)
                
                latency = time.time() - start_time
                st.info(f"Search completed in {latency:.2f}s")
                
                display_results(results, query_text, generated_response)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.error("Full error details:")
                st.code(traceback.format_exc())
                st.info("Please try rephrasing your question or contact support.")  # HINT: "Please try rephrasing your question or contact support."

elif search_button and not query_text:
    st.warning("Please enter a travel question.")  # HINT: "Please enter a travel question."

# Add a test section to verify the application is working
if st.sidebar.button("Test Application"):
    st.sidebar.success("Application is running successfully!")
    if engine:
        st.sidebar.success("Search engine is initialized!")
    else:
        st.sidebar.error("Search engine failed to initialize!")
