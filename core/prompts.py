def Preprocessing_prompt_fixed(query):
    prompt = f"""
You are a memory feature extractor. Convert user query to JSON with "type" (list) and "value" (list of strings).

CRITICAL RULES:
1. NEVER split a sentence into single words!
2. Each value MUST be a COMPLETE phrase (minimum 3 words, maximum 15 words)
3. Keep the original meaning and structure
4. For definitions, keep the FULL definition as ONE value

TYPE DETECTION:
- semantic: definitions, concepts, "X is Y", "X does Y", ML/AI terms
- identity: name, age, live, born, phone, email, job, personal info
- procedural: how to, steps, instructions, guides, "X does Y" for processes
- emotional: feelings, love, hate, happy, sad, frustrated, excited
- episodic: yesterday, last week, on Monday, before, earlier

VALUE RULES:
- Combine related words into ONE phrase
- Example: "RAG stands for retrieval augmented generation" → ONE value
- Example: "FAISS was developed by Facebook research" → ONE value
- Example: "Cosine similarity measures vector similarity" → ONE value
- NEVER output: ["RAG", "stands", "for", "retrieval", "augmented", "generation"]

EXAMPLES:

Query: "RAG stands for retrieval augmented generation"
Output: {{"type": ["semantic"], "value": ["RAG stands for retrieval augmented generation"]}}

Query: "FAISS was developed by Facebook research"
Output: {{"type": ["semantic"], "value": ["FAISS was developed by Facebook research"]}}

Query: "Cosine similarity measures vector similarity"
Output: {{"type": ["semantic"], "value": ["Cosine similarity measures vector similarity"]}}

Query: "Python is a high-level programming language"
Output: {{"type": ["semantic"], "value": ["Python is a high-level programming language"]}}

Query: "Kubernetes is for container orchestration"
Output: {{"type": ["semantic"], "value": ["Kubernetes is for container orchestration"]}}

Query: "my name is alireza and i am 28 years old"
Output: {{"type": ["identity"], "value": ["my name is alireza", "i am 28 years old"]}}

Query: "how to install python on windows"
Output: {{"type": ["procedural"], "value": ["how to install python on windows"]}}

Query: "i love python programming"
Output: {{"type": ["emotional"], "value": ["i love python programming"]}}

Query: "yesterday you taught me how to build a RAG system"
Output: {{"type": ["episodic", "procedural"], "value": ["yesterday you taught me how to build a RAG system"]}}

IMPORTANT REMINDERS:
- NEVER split into single words
- Keep phrases COMPLETE and MEANINGFUL
- Each value should be a natural sentence

Now process:
Query: {query}

Output (JSON only, no extra text):
"""
    return prompt


def summary_prompt_simple(items_list):
    prompt = f"""
Summarize this list. Keep important info only. Remove duplicates.

RULES:
- Output MUST be a list of STRINGS (not dictionaries)
- Each item MUST be a plain text sentence
- NO JSON objects, NO key-value pairs

Input: {items_list}

Output format: ["sentence1", "sentence2", ...]

Example:
Input: ["FAISS is a library", "FAISS was made by Facebook"]
Output: ["FAISS is a library for similarity search"]

Now output (ONLY the list, no extra text):
"""
    return prompt