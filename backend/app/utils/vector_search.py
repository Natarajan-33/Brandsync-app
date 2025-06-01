from sentence_transformers import SentenceTransformer
import chromadb
from typing import List, Dict, Any

class VectorSearch:
    """Utility class for vector search operations"""
    
    def __init__(self, collection_name: str = "influencers", model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the vector search utility
        
        Args:
            collection_name: Name of the ChromaDB collection
            model_name: Name of the sentence transformer model to use
        """
        self.model = SentenceTransformer(model_name)
        self.chroma_client = chromadb.Client()
        
        # Create or get the collection
        try:
            self.collection = self.chroma_client.create_collection(name=collection_name)
        except ValueError:
            # Collection already exists
            self.collection = self.chroma_client.get_collection(name=collection_name)
    
    def add_items(self, items: List[Dict[str, Any]], id_field: str = "id", text_generator=None):
        """Add items to the vector database
        
        Args:
            items: List of items to add
            id_field: Field to use as the unique identifier
            text_generator: Function to generate text for embedding from an item
        """
        if not items:
            return
            
        # Generate IDs and texts for embedding
        ids = [str(item[id_field]) for item in items]
        
        # Generate text for embedding
        if text_generator:
            texts = [text_generator(item) for item in items]
        else:
            # Default text generation - concatenate all string values
            texts = []
            for item in items:
                text_parts = []
                for key, value in item.items():
                    if isinstance(value, str):
                        text_parts.append(f"{key}: {value}")
                    elif isinstance(value, list) and all(isinstance(x, str) for x in value):
                        text_parts.append(f"{key}: {', '.join(value)}")
                texts.append(" ".join(text_parts))
        
        # Generate embeddings
        embeddings = self.model.encode(texts).tolist()
        
        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=items
        )
    
    def search(self, query: str, top_k: int = 5):
        """Search for items similar to the query
        
        Args:
            query: The search query
            top_k: Number of results to return
            
        Returns:
            List of matching items
        """
        # Encode the query
        query_embedding = self.model.encode(query).tolist()
        
        # Search in the collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Extract and return the matched items
        if results and "metadatas" in results and results["metadatas"]:
            return results["metadatas"][0]  # First query results
        
        return []
