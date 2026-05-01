from Memory.High_level_memory import Save_memory, Search_memory, save_memory_to_disk, load_memory_from_disk
from Memory.Low_level_memory import search_memory as LowSearch, persist_memory, load_persisted_memory, add_to_memory
from Utils.logger import get_logger
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import asyncio
import uuid
import time 

logger = get_logger("MEM")
logger.info("MemoryManager started")

class MemoryManager:
    def __init__(self,gen, STM_SIZE: int = 15):  
        self.gen = gen
        self.stm = deque(maxlen=STM_SIZE)
        self.stm_size = STM_SIZE
    
    def add_interaction(self, user_input: str, assistant_output: str = ''):
        
        
        if len(user_input) >= 500:
            encoded = self.gen.Encode(user_input + ' ' + assistant_output)
            if encoded is not None:
                metadata = {
                    "text": f"{user_input} {assistant_output}",
                    "importance": 0.8,  # SOLID
                    "timestamp": time.time()
                }
                add_to_memory(encoded, uuid.uuid4(), metadata)
        
    
        stm_list = list(self.stm)
        new_stm_list = Save_memory(stm_list, user_input,self.gen, assistant_output)
        
        self.stm = deque(new_stm_list, maxlen=self.stm_size)
        logger.info(f"Added: {user_input[:50]}...")

    def search(self, query: str, efficient: bool = True):  
        if efficient:
            return LowSearch(query,self.gen)
        else:
            if len(query) >= 500:
                return LowSearch(query,self.gen)
            else:
                return Search_memory(query,self.gen)

    def get_stm_context(self, last_n: int = 0):
        if last_n:
            return "\n".join(list(self.stm)[-last_n:])
        return "\n".join(self.stm)

    def get_relevant_memory(self, query: str):
        return {
            'stm': self.get_stm_context(last_n=5),
            'ltm': self.search(query, efficient=False)  
        }

    def save_all(self):
        save_memory_to_disk()
        persist_memory()
        logger.info("All saved")

    def load_all(self):
        load_memory_from_disk()
        load_persisted_memory()
        logger.info("All loaded")

    def clear_stm(self):
        self.stm.clear()
        logger.info("STM cleared")

    def get_stats(self):
        return {
            'stm_size': len(self.stm),
            'stm_max': self.stm_size
        }
    # NOT COMPLETE
    def ForgettingSystem(self):
        from Memory.High_level_memory import LTM_index , LTM_text
        logger.info(f"Forgetting Started for {len(LTM_text)} items")
        delete_ids = []
        memory_types = []
        logger.info("Searching For Low RANK")
        for ID in LTM_text:
            item = LTM_text[ID]
            if item.rank < 0.2:
                delete_ids.append(ID)
                memory_types.append(item.type)

        logger.info(f"Removing {len(delete_ids)} low rank memories")
        for ids ,type in zip(delete_ids , memory_types):
            del LTM_text[ids]
            LTM_index[type].remove_ids(ids)










logger.info("MemoryManager ready")
