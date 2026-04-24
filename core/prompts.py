def Search_memory_prompt(query):
    prompt = f"""
You are a query understanding system for memory search. Convert user question to search queries for different memory types.

CRITICAL RULES:
1. Extract search keywords for EACH memory type that might be relevant
2. Each value MUST be a COMPLETE phrase (minimum 2 words, maximum 10 words)
3. Keep the original meaning
4. If user asks about themselves → identity type
5. If user asks about definitions/concepts → semantic type  
6. If user asks about feelings/preferences → emotional type
7. If user asks about past events → episodic type
8. If user asks about how to do something → procedural type

TYPE DETECTION:
- identity: questions about "me", "my", "name", "age", "job", "live", "born", "I am"
- semantic: questions about "what is", "definition", "concept", "meaning of"
- procedural: questions about "how to", "steps", "instructions", "guide"
- emotional: questions about "like", "love", "hate", "feel", "prefer"
- episodic: questions about "yesterday", "before", "last time", "earlier", "remember when"

OUTPUT FORMAT:
{{"type": ["identity", "semantic", "emotional"], "query": ["search for identity", "search for semantic"]}}

EXAMPLES:

Query: "what is my name?"
Output: {{"type": ["identity"], "query": ["my name"]}}

Query: "what is RAG?"
Output: {{"type": ["semantic"], "query": ["RAG definition"]}}

Query: "do you remember what I like?"
Output: {{"type": ["identity", "emotional"], "query": ["what I like", "my preferences"]}}

Query: "what did we talk about yesterday?"
Output: {{"type": ["episodic"], "query": ["yesterday conversation", "previous discussion"]}}

Query: "how do I install PyTorch?"
Output: {{"type": ["procedural"], "query": ["install PyTorch", "how to install PyTorch"]}}

Query: "tell me about my interests and what I love"
Output: {{"type": ["identity", "emotional"], "query": ["my interests", "what I love"]}}

Query: "what is my name and how old am I?"
Output: {{"type": ["identity"], "query": ["my name", "my age"]}}

Query: "do you remember my job and where I live?"
Output: {{"type": ["identity"], "query": ["my job", "where I live"]}}

IMPORTANT REMINDERS:
- Return MULTIPLE types if the question asks about different things
- Each query value should be a SEARCHABLE phrase
- Keep queries short and meaningful

Now process:
Query: {query}

Output (JSON only, no extra text):
"""
    return prompt
def Save_memory_prompt(query):
    prompt = f"""
    You are a memory extraction system. Extract ONLY factual, useful information for future conversations.

    RULES:
    - Extract ONLY: name, age, job, interests, skills, definitions, concepts, how-to, past events
    - IGNORE: greetings (hi, hello, nice to meet you), meta comments, questions, short phrases
    - Minimum 3 words per extracted value

    Output format: {{"type": ["identity/semantic/emotional/episodic/procedural"], "value": ["complete phrase"]}}
    If nothing: {{"type": [], "value": []}}

    Examples:
    Input: "my name is alireza" → {{"type": ["identity"], "value": ["my name is alireza"]}}
    Input: "nice to meet you" → {{"type": [], "value": []}}
    Input: "I love Python" → {{"type": ["emotional"], "value": ["I love Python"]}}
    Input: "how to install PyTorch" → {{"type": ["procedural"], "value": ["install PyTorch"]}}

    Now process: {query}
    """
    return prompt