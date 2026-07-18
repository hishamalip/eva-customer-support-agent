# Import required libraries for vector database operations, embeddings, and JSON handling
from chromadb import PersistentClient, EmbeddingFunction, Embeddings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from typing import List
import json

# Configuration constants for the vector store
# MODEL_NAME: The HuggingFace embedding model to use for generating vector embeddings
# DB_PATH: Local directory path where ChromaDB will persist the vector database
# FAQ_FILE_PATH: Path to the JSON file containing FAQ question-answer pairs
# INVENTORY_FILE_PATH: Path to the JSON file containing product inventory data
MODEL_NAME = 'NovaSearch/stella_en_1.5B_v5'
DB_PATH = './.chroma_db'
FAQ_FILE_PATH = './FAQ.json'
INVENTORY_FILE_PATH = './inventory.json'


class Product:
    """Simple product metadata container for inventory items."""

    def __init__(self, name: str, description: str, type: str, price: float, quantity: int):
        # Initialize product with its metadata attributes
        self.name = name
        self.description = description
        self.type = type
        self.price = price
        self.quantity = quantity


class QuestionPair:
    """Represents a question-and-answer pair for FAQ entries."""

    def __init__(self, question: str, answer: str):
        # Initialize FAQ entry with question and its corresponding answer
        # Note: There appears to be a typo - 'questions' should likely be 'question' to match the parameter
        self.questions = question
        self.answer = answer


class CustomEmbeddingClass(EmbeddingFunction):
    """Custom embedding function that wraps HuggingFace embedding model for ChromaDB."""

    def __init__(self):
        # Initialize the HuggingFace embedding model with the specified model name
        self.embedding_model = HuggingFaceEmbedding(model_name=MODEL_NAME)

    def __call__(self, input_texts: List[str]) -> Embeddings:
        # Generate embeddings for a list of input texts
        # Returns a list of embedding vectors corresponding to each input text
        return [self.embedding_model.get_text_embeddings(text) for text in input_texts]
    

class FlowerShopVectorStore:
    """Main vector store class for managing FAQ and inventory collections for a flower shop.
    
    Uses ChromaDB as the vector database backend with HuggingFace embeddings.
    Automatically loads data from JSON files if collections are empty.
    """

    def __init__(self):
        # Initialize ChromaDB persistent client with the configured database path
        db = PersistentClient(path=DB_PATH)
        custom_embedding_function = CustomEmbeddingClass()

        # Create or retrieve existing collections for FAQ and Inventory
        self.faq_collection = db.get_or_create_collection(name="FAQ", embedding_function=custom_embedding_function)
        self.inventory_collection = db.get_or_create_collection(name="Inventory", embedding_function=custom_embedding_function)

        # Load data into collections if they are empty
        if self.faq_collection.count() == 0:
            self._load_faq_collection(FAQ_FILE_PATH)

        if self.inventory_collection.count() == 0:
            self._load_inventory_collection(INVENTORY_FILE_PATH)


    def _load_faq_collection(self, faq_file_path: str):
        """Load FAQ data from JSON file into the FAQ collection.
        
        Args:
            faq_file_path: Path to the JSON file containing FAQ data
        """
        # Open and parse the FAQ JSON file
        with open(faq_file_path, "r") as f:
            faqs = json.load(f)

        # Add both questions and answers as separate documents to the collection
        # This allows searching against both questions and their answers
        self.faq_collection.add(
            documents = [faq["question"] for faq in faqs] + [faq["answer"] for faq in faqs],
            ids = [str(i) for i in range(len(faqs) * 2)],  # Generate unique IDs for each document
            metadatas = 2*faqs  # Duplicate metadata to match the doubled documents list
        )


    def _load_inventory_collection(self, inventory_file_path: str):
        """Load inventory data from JSON file into the Inventory collection.
        
        Args:
            inventory_file_path: Path to the JSON file containing inventory data
        """
        # Open and parse the inventory JSON file
        with open(inventory_file_path, "r") as f:
            inventories = json.load(f)
    
        # Add product descriptions as documents to the collection
        # Each document is indexed with its full metadata for retrieval
        self.inventory_collection.add(
            documents = [inventory["description"] for inventory in inventories],
            ids = [str(i) for i in range(len(inventories))],  # Generate unique IDs for each product
            metadatas = inventories  # Store full product metadata with each document
        )


    def query_faqs(self, query: str):
        """Query the FAQ collection for similar questions/answers.
        
        Args:
            query: The search query string
            
        Returns:
            Query results containing the top 5 most similar FAQ entries with their scores and metadata
        """
        return self.faq_collection.query(query_texts=[query], n_results=5)
    
    def query_inventory(self, query: str):
        """Query the Inventory collection for similar products.
        
        Args:
            query: The search query string
            
        Returns:
            Query results containing the top 5 most similar inventory items with their scores and metadata
        """
        return self.inventory_collection.query(query_texts=[query], n_results=5)
