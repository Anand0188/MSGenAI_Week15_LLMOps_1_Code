"""
RAGAS Evaluation Script for Travel Chatbot
"""

import json
import logging
from pathlib import Path

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

from datasets import Dataset

from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

from src.search_engine import TravelSearchEngine
from src.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ragas_eval")


class RagasEvaluator:

    def __init__(self):

        self.engine = TravelSearchEngine()
        self.dataset_path = Path("data/golden_dataset.json")

    # -----------------------------
    # Load or create dataset
    # -----------------------------

    def load_dataset(self):

        if not self.dataset_path.exists():

            logger.info("Creating sample golden dataset")

            dataset = [
                {
                    "question": "What is baggage allowance for international flights?",
                    "ground_truth": "Economy passengers can carry one checked bag up to 23kg and one cabin bag up to 7kg."
                },
                {
                    "question": "Do Indians need visa for UK travel?",
                    "ground_truth": "Yes, Indian citizens require a visa to travel to the United Kingdom."
                },
                {
                    "question": "What documents are required for international travel?",
                    "ground_truth": "You need a valid passport, visa if required, and flight tickets."
                },
                {
                    "question": "What is Air India's cancellation policy?",
                    "ground_truth": "Air India allows cancellation depending on fare type and timing before departure."
                },
                {
                    "question": "What is the refund policy for cancelled flights?",
                    "ground_truth": "Refund eligibility depends on airline policies and fare rules."
                }
            ]

            self.dataset_path.parent.mkdir(exist_ok=True)

            with open(self.dataset_path, "w") as f:
                json.dump(dataset, f, indent=2)

        with open(self.dataset_path) as f:
            return json.load(f)

    # -----------------------------
    # Generate chatbot answers
    # -----------------------------

    def generate_answers(self, questions):

        answers = []
        contexts = []

        for q in questions:

            logger.info(f"Generating answer for: {q}")

            try:

                docs, _ = self.engine.search_by_text(q, k=3)

                answer = self.engine.synthesize_response(docs, q)

                context_texts = [doc.page_content for doc in docs]

                answers.append(answer)
                contexts.append(context_texts)

            except Exception as e:

                logger.error(e)

                answers.append("Error generating answer")
                contexts.append([])

        return answers, contexts

    # -----------------------------
    # Run RAGAS evaluation
    # -----------------------------

    def run(self):

        logger.info("Starting RAGAS evaluation")

        data = self.load_dataset()

        questions = [d["question"] for d in data]

        ground_truths = [[d["ground_truth"]] for d in data]

        answers, contexts = self.generate_answers(questions)

        dataset = Dataset.from_dict(
            {
                "question": questions,
                "answer": answers,
                "contexts": contexts,
                "ground_truths": ground_truths,
            }
        )

        # -----------------------------
        # Azure OpenAI LLM
        # -----------------------------

        llm = AzureChatOpenAI(
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
            azure_deployment=Config.AZURE_OPENAI_DEPLOYMENT_NAME,
            api_key=Config.AZURE_OPENAI_API_KEY,
            api_version=Config.AZURE_OPENAI_API_VERSION,
            temperature=0,
        )

        # -----------------------------
        # Azure OpenAI Embeddings
        # -----------------------------

        embeddings = AzureOpenAIEmbeddings(
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
            azure_deployment=Config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
            api_key=Config.AZURE_OPENAI_API_KEY,
            api_version=Config.AZURE_OPENAI_API_VERSION,
        )

        logger.info("Running RAGAS metrics")

        results = evaluate(
            dataset,
            metrics=[
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall,
            ],
            llm=LangchainLLMWrapper(llm),
            embeddings=LangchainEmbeddingsWrapper(embeddings),
            raise_exceptions=False,
        )

        logger.info("Evaluation completed")

        print("\nEvaluation Results\n")
        print(results)

        self.save_results(results)

        return results

    # -----------------------------
    # Save results
    # -----------------------------

    def save_results(self, results):

        output_dir = Path("reports")

        output_dir.mkdir(exist_ok=True)

        summary = {
            "faithfulness": float(results["faithfulness"]),
            "answer_relevancy": float(results["answer_relevancy"]),
            "context_precision": float(results["context_precision"]),
            "context_recall": float(results["context_recall"]),
        }

        with open(output_dir / "evaluation_summary.json", "w") as f:
            json.dump(summary, f, indent=2)

        logger.info("Results saved to reports/evaluation_summary.json")


# -----------------------------
# Run Script
# -----------------------------

        # Save detailed results CSV
        import pandas as pd
        
        # Create detailed dataset for CSV
        data = self.load_dataset()
        questions = [d["question"] for d in data]
        ground_truths = [d["ground_truth"] for d in data]
        answers, contexts = self.generate_answers(questions)
        
        detailed_data = {
            "question": questions,
            "ground_truth": ground_truths,
            "answer": answers,
            "contexts": [" | ".join(ctx) for ctx in contexts]
        }
        
        detailed_df = pd.DataFrame(detailed_data)
        detailed_df.to_csv(output_dir / "evaluation_detailed.csv", index=False)
        
        logger.info("✅ Detailed results saved to reports/evaluation_detailed.csv")

        # Save category breakdown
        category_breakdown = {
            "total_questions": len(questions),
            "metrics": {
                "faithfulness": float(results["faithfulness"]),
                "answer_relevancy": float(results["answer_relevancy"]),
                "context_precision": float(results["context_precision"]),
                "context_recall": float(results["context_recall"])
            }
        }
        
        with open(output_dir / "category_breakdown.json", "w") as f:
            json.dump(category_breakdown, f, indent=2)
            
        logger.info("✅ Category breakdown saved to reports/category_breakdown.json")
        # -----------------------------
# Run Script
# -----------------------------

if __name__ == "__main__":

    evaluator = RagasEvaluator()

    evaluator.run()
