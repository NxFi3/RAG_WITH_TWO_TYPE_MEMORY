import re 
from Utils.logger import get_logger
import json


logger = get_logger("PRR")
logger.info("PARSER started")



class ParserManager:
    def __init__(self) -> None:
        pass

    def clean_json_string(self,text: str) -> str:
        """Fix common JSON issues"""
        if not text:
            return ""
        
        text = re.sub(r"```json\s*|\s*```", "", text)
        text = re.sub(r"```\w*\s*|\s*```", "", text)
        
    
        text = text.replace("“", '"').replace("”", '"')
        text = text.replace("'", '"')  
    
        text = re.sub(r',\s*}', '}', text)
        text = re.sub(r',\s*]', ']', text)
        
        
        text = re.sub(r'//.*?\n', '\n', text)
        
        return text.strip()

    def extract_json(self,text: str):
        """Extract first valid JSON object using bracket counting"""
        if not text:
            return None

        start = text.find('{')
        if start == -1:
            return None
        
        bracket_count = 0
        in_string = False
        escape = False
        
        for i in range(start, len(text)):
            char = text[i]
            
            if escape:
                escape = False
                continue
            
            if char == '\\':
                escape = True
                continue
            
            if char == '"' and not escape:
                in_string = not in_string
                continue
            
            if not in_string:
                if char == '{':
                    bracket_count += 1
                elif char == '}':
                    bracket_count -= 1
                    if bracket_count == 0:
                        json_str = text[start:i+1]
                        try:
                            return json.loads(json_str)
                        except:
                            break
        
        
        matches = re.findall(r'\{[^{}]*"type"\s*:\s*\[.*?\]\s*,\s*"value"\s*:\s*(?:null|"[^"]*")\s*\}', text, re.DOTALL)
        for m in matches:
            try:
                return json.loads(m)
            except:
                continue
        
        return None
    def OutputManage(self, text: str):
        if not text or len(text.strip()) == 0:
            logger.warning("Empty output from LLM")
            return {'type': 'error', 'message': 'empty output', 'Memory': [], 'Query': None}
        
        data = None
        try:
            data = json.loads(text)
        except:
            pass
        
        if data is None:
            try:
                cleaned = self.clean_json_string(text)
                data = json.loads(cleaned)
            except:
                pass
        
        if data is None:
            data = self.extract_json(text)
        
        if data is None:
            logger.warning(f"Could not parse JSON from: {text[:200]}")
            return {'type': 'error', 'message': 'no json found', 'Memory': [], 'Query': None}
    
        memory_types = data.get("Memory", [])
        value = data.get("value", [])
        

        if not memory_types:
            memory_types = data.get("type", [])
        
        if isinstance(memory_types, str):
            memory_types = [memory_types]

        if not value:
            return {'type': 'success', 'Memory': memory_types, 'Query': None}
        
        return {
            'type': 'success',
            'Memory': memory_types,
            'Query': value
        }