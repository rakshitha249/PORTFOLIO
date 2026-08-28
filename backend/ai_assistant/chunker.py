import os

class TextChunker:
    """
    A service for chunking text into smaller semantic pieces.
    """
    def __init__(self, chunk_size=None, chunk_overlap=None):
        self.chunk_size = chunk_size or int(os.environ.get('RAG_CHUNK_SIZE', 500))
        self.chunk_overlap = chunk_overlap or int(os.environ.get('RAG_CHUNK_OVERLAP', 50))
        
        if self.chunk_size <= self.chunk_overlap:
            raise ValueError("Chunk size must be greater than chunk overlap.")

    def chunk_text(self, text):
        """
        Splits text into overlapping chunks, attempting to respect word boundaries.
        Returns a list of string chunks.
        """
        if not text:
            return []
            
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            previous_start = start
            end = start + self.chunk_size
            
            if end >= text_length:
                chunk = text[start:text_length].strip()
                if chunk:
                    chunks.append(chunk)
                break
                
            # Try to find a good breaking point near the end
            search_window_start = max(start + 1, end - int(self.chunk_size * 0.2))
            
            newline_pos = text.rfind('\n', search_window_start, end)
            if newline_pos != -1:
                break_point = newline_pos
            else:
                space_pos = text.rfind(' ', search_window_start, end)
                if space_pos != -1:
                    break_point = space_pos
                else:
                    break_point = -1
                    
            if break_point != -1:
                end = break_point + 1
                
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
                
            start = end - self.chunk_overlap
            
            # Prevent infinite loops if we didn't advance
            if start <= previous_start:
                 start = previous_start + self.chunk_size - self.chunk_overlap
                
        return chunks
