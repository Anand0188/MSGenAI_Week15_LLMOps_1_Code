import mlflow
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from src.config import Config
from governance.governance_gate import GovernanceGate
from src.vector_store import get_vector_store


class TravelSearchEngine:

    def __init__(self):

        self.governance_gate = GovernanceGate()

        self.llm = AzureChatOpenAI(
            api_key=Config.AZURE_OPENAI_API_KEY,
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
            api_version=Config.AZURE_OPENAI_API_VERSION,
            deployment_name=Config.AZURE_OPENAI_DEPLOYMENT_NAME,
            temperature=0.7
        )

        self.embeddings = AzureOpenAIEmbeddings(
            api_key=Config.AZURE_OPENAI_API_KEY,
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
            azure_deployment=Config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME,
            api_version=Config.AZURE_OPENAI_API_VERSION,
        )

        self.vector_store = get_vector_store(self.embeddings)

    def search_by_text(self, query_text: str, k: int = 5):

        mlflow.set_experiment(Config.MLFLOW_EXPERIMENT_NAME)

        with mlflow.start_run(run_name="search_travel_info", nested=True):

            gov_check = self.governance_gate.validate_input(query_text)

            if not gov_check['is_valid']:
                mlflow.log_param("governance_failed", True)
                mlflow.log_param("violations", str(gov_check['violations']))
                return [], query_text

            mlflow.log_param("query_text", query_text)
            mlflow.log_param("k", k)

            docs = self.vector_store.similarity_search(query_text, k=k, search_type="hybrid")

            mlflow.log_metric("results_count", len(docs))

            return docs, query_text

    def search(self, query_text: str, k: int = 5):
        """
        Wrapper used by ingestion verification
        """
        return self.search_by_text(query_text, k)

    def synthesize_response(self, docs, user_query):

        mlflow.set_experiment(Config.MLFLOW_EXPERIMENT_NAME)

        with mlflow.start_run(run_name="synthesize_response", nested=True):

            if not docs:
                return "I don't have enough information to answer that question. Please try asking something else."

            context = "\n".join([
                f"- {doc.page_content} (Source: {doc.metadata.get('source', 'Unknown')})"
                for doc in docs
            ])

            prompt = f"""
You are a helpful travel assistant for Wanderlust Travels.

Knowledge Base Information:
{context}

Customer Question: "{user_query}"

Provide a clear and helpful answer using the information above.
"""

            response = self.llm.invoke(prompt).content

            gov_check = self.governance_gate.validate_output(response)

            if not gov_check['is_valid']:
                return "I generated a response but it didn't pass safety checks."

            mlflow.log_text(response, "final_response.txt")

            return response