from Utils.logger import get_logger
from sentence_transformers import SentenceTransformer
import numpy as np
logger = get_logger("EMB")
logger.info("Embedding Service startup")

try:
    encoder = SentenceTransformer("D:\SentenceTransformer Model")
except Exception as e:
    logger.error("Error While Loading Embedding Encoder")
    logger.error(f"Error: {e}")
    

def GetEmbedding(Query:str) -> np.ndarray:
    try:
        Embedding = encoder.encode(Query,normalize_embeddings=True).reshape(1,-1)
        
    except Exception as e:
        logger.error("Error While Getting Embedding ")
        logger.error(f"Error: {e}")
        return None 
    return Embedding