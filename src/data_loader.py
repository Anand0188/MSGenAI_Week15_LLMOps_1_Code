import os
import pandas as pd
from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

DATA_DIR = Path("data")


class TravelDataLoader:
    """Loads travel documents (PDFs, CSVs) from data directory"""

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )

    def load_pdfs_from_data_directory(self) -> List[Document]:

        documents = []

        if not DATA_DIR.exists():
            print(f"Warning: Directory {DATA_DIR} does not exist")
            return documents

        pdf_files = list(DATA_DIR.glob("*.pdf"))
        print(f"Found {len(pdf_files)} PDF files in data/")

        for pdf_file in pdf_files:
            try:
                loader = PyPDFLoader(str(pdf_file))
                docs = loader.load()

                for doc in docs:
                    doc.metadata.update({
                        "source": pdf_file.name,
                        "file_type": "pdf"
                    })

                documents.extend(docs)

                print(f"  ✓ Loaded: {pdf_file.name} ({len(docs)} pages)")

            except Exception as e:
                print(f"  ✗ Error loading {pdf_file.name}: {e}")

        return documents

    def load_csvs_from_data_directory(self) -> List[Document]:

        documents = []

        if not DATA_DIR.exists():
            print(f"Warning: Directory {DATA_DIR} does not exist")
            return documents

        csv_files = list(DATA_DIR.glob("*.csv"))
        print(f"Found {len(csv_files)} CSV files in data/")

        for csv_file in csv_files:
            try:
                df = pd.read_csv(str(csv_file))

                for idx, row in df.iterrows():

                    content = " | ".join(
                        f"{col}: {val}" for col, val in row.items()
                    )

                    documents.append(
                        Document(
                            page_content=content,
                            metadata={
                                "source": csv_file.name,
                                "file_type": "csv",
                                "row_index": idx
                            }
                        )
                    )

                print(f"  ✓ Loaded: {csv_file.name} ({len(df)} rows)")

            except Exception as e:
                print(f"  ✗ Error loading {csv_file.name}: {e}")

        return documents

    def load_all_travel_documents(self) -> List[Document]:

        all_documents = []

        print("\n📂 Loading travel knowledge base...")
        print("=" * 60)

        pdf_docs = self.load_pdfs_from_data_directory()
        all_documents.extend(pdf_docs)

        csv_docs = self.load_csvs_from_data_directory()
        all_documents.extend(csv_docs)

        print("=" * 60)
        print(f"✅ Total documents loaded: {len(all_documents)}")

        return all_documents

    def load_documents(self) -> List[Document]:

        documents = self.load_all_travel_documents()

        chunks = self.split_documents(documents)

        return chunks

    def split_documents(self, documents: List[Document]) -> List[Document]:

        print(f"\n✂️ Splitting {len(documents)} documents into chunks...")

        chunks = self.text_splitter.split_documents(documents)

        clean_chunks = []

        for chunk in chunks:

            metadata = {k: str(v) for k, v in chunk.metadata.items()}

            clean_chunks.append(
                Document(
                    page_content=chunk.page_content,
                    metadata=metadata
                )
            )

        print(f"✅ Created {len(clean_chunks)} chunks")

        print(
            f"Average chunk size: "
            f"{sum(len(c.page_content) for c in clean_chunks) // max(len(clean_chunks), 1)} chars"
        )

        return clean_chunks


if __name__ == "__main__":
    loader = TravelDataLoader()
    chunks = loader.load_documents()

    print("\n📊 Summary:")
    print(f"Total chunks: {len(chunks)}")