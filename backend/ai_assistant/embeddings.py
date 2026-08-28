import os
import abc
import random
import logging

logger = logging.getLogger(__name__)

class EmbeddingService(abc.ABC):
    @abc.abstractmethod
    def get_embedding(self, text: str) -> list[float]:
        pass
        
    @abc.abstractmethod
    def get_dimension(self) -> int:
        pass

class MockEmbeddingService(EmbeddingService):
    def __init__(self, dimension=768):
        self.dimension = dimension
        
    def get_embedding(self, text: str) -> list[float]:
        # Deterministic random embedding based on hash
        import hashlib
        seed = int(hashlib.md5(text.encode()).hexdigest(), 16)
        random.seed(seed)
        return [random.uniform(-1, 1) for _ in range(self.dimension)]
        
    def get_dimension(self) -> int:
        return self.dimension

class GeminiEmbeddingService(EmbeddingService):
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
            
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        # Using text-embedding-004 which outputs 768 dimensions
        self.model = 'models/text-embedding-004'
        self.dimension = 768

    def get_embedding(self, text: str) -> list[float]:
        import google.generativeai as genai
        try:
            result = genai.embed_content(
                model=self.model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Error getting embedding from Gemini: {e}")
            raise

    def get_dimension(self) -> int:
        return self.dimension

def get_embedding_service() -> EmbeddingService:
    provider = os.environ.get('RAG_EMBEDDING_PROVIDER', 'mock').lower()
    
    if provider == 'gemini':
        try:
            return GeminiEmbeddingService()
        except ValueError as e:
            logger.warning(f"Falling back to mock embedding: {e}")
            return MockEmbeddingService()
    
    return MockEmbeddingService()
