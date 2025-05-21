import numpy as np

class EmbeddingService:
    def generate_embedding(self, file_content: bytes):
        # Dummy embedding: return a fixed vector
        return np.random.rand(10).tolist() 