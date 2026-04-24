# agent.py
from Memory.Memory_manager import MemoryManager
from core.generator import GeneratorManager

class Agent:
    def __init__(self):
        self.memory = MemoryManager(STM_SIZE=15)
        self.generator = GeneratorManager()
        self.memory.load_all()
    
    def chat(self, user_input: str) -> str:
        # 1. گرفتن حافظه مرتبط
        context = self.memory.get_relevant_memory(user_input)
        
        # 2. ساخت prompt
        prompt = f"""
Previous conversation:
{context['stm']}

Relevant memories:
{context['ltm']}

User: {user_input}
Assistant:"""
        
        # 3. تولید پاسخ
        response = self.generator.generator(prompt)
        
        # 4. ذخیره در حافظه
        self.memory.add_interaction(user_input, response)
        
        return "AI: "+response
    
    def save(self):
        self.memory.save_all()

# استفاده
agent = Agent()
while True:
    inputs = input("You: ")
    print(agent.chat(inputs))
    agent.save()