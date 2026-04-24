import time 
import uuid
import math
import numpy as np

class MemoryItem:
    def __init__(self, memory_type: list, value: str, embedding: np.ndarray, importance: float=0.6):
        
        self.ID = uuid.uuid4().int & 0x7FFFFFFFFFFFFFFF
        self.Memory_type = memory_type
        self.Value = value
        self.Embedding = embedding
        self.Importance = importance
        self.Frequency = 1
        self.Created_at = time.time()
        self.last_access = time.time()
        self.Rank = self._calculate_rank() 
    
    def _get_recency_score(self, decay: float = 0.5) -> float:
        hours_ago = (time.time() - self.last_access) / 3600
        half_life_hours = 24 / (1 - decay)
        return 0.5 ** (hours_ago / half_life_hours)
    
    def _get_frequency_score(self) -> float:
        return math.log(self.Frequency + 1) / math.log(10)
    
    def _calculate_rank(self, decay: float = 0.5) -> float:  
        recency_score = self._get_recency_score(decay)
        freq_score = self._get_frequency_score()
        
        
        return (self.Importance * 0.6 + 
                recency_score * 0.2 + 
                freq_score * 0.2)
    
    def update(self, decay: float = 0.5):
        self.Frequency += 1
        self.last_access = time.time()
        self.Rank = self._calculate_rank(decay)  
    
    def to_dict(self):
        return {
            "id": self.ID,
            "type": self.Memory_type,
            "value": self.Value,
            "importance": self.Importance,
            "frequency": self.Frequency,
            "rank": self.Rank,
            "created_at": self.Created_at,
            "last_access": self.last_access
        }