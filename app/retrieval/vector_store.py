from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from typing import List, Dict, Any
import os

class VectorStoreService:
    """
    Manages session-based local vector storage using FAISS and Ollama.
    """
    
    def __init__(self, model_name: str = "nomic-embed-text"):
        self.embeddings = OllamaEmbeddings(model=model_name)
        self.stores = {} # session_id -> FAISS index

    def create_session_store(self, session_id: str, texts: List[str], metadatas: List[Dict[str, Any]]):
        """
        Creates and stores a FAISS index for a specific investigation session.
        """
        vector_store = FAISS.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas
        )
        self.stores[session_id] = vector_store
        return vector_store

    def query(self, session_id: str, query_text: str, k: int = 4):
        """
        Performs similarity search against a session's vector store.
        """
        if session_id not in self.stores:
            raise KeyError(f"No vector store found for session {session_id}")
            
        store = self.stores[session_id]
        results = store.similarity_search(query_text, k=k)
        return results

    def delete_session_store(self, session_id: str):
        """
        Removes a session's vector store from memory.
        Part of the 'Zero-Persistence' privacy policy.
        """
        if session_id in self.stores:
            del self.stores[session_id]
