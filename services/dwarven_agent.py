from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.messages import SystemMessage, HumanMessage

# Initialize the LLM (connecting to Ollama running locally)
llm = ChatOllama(
    # model = "qwen3:4b",
    model="pedrolucas/smollm3:3b-q4_k_m",
    # model="schroneko/smollm-135m:q4_0",
    # model="smollm2:360m",
    # model="smollm2:135m",   
    # model="tinyllama",
    temperature=0.6,      # Balanced
    top_p=0.95,
    num_predict=1000
    # reasoning=True
)

def build_dwarven_prompt(frustration_level: int = 1, conversation_history: list = None, current_page: int = 0, total_pages: int = 1) -> ChatPromptTemplate:
    """Build a dynamic prompt based on frustration level and conversation context."""
    
    # Define tone escalation
    tone_instructions = {
        1: "You are cheerful and helpful. Be silly, charming, and enthusiastic.",
        2: "You are getting slightly annoyed. Show mild irritation but still helpful. Sigh a bit.",
        3: "You are frustrated. Your patience is wearing thin. Be grumpy but keep helping.",
        4: "You are exhausted and angry. This is your FINAL offer. Make a strong recommendation."
    }
    
    # Determine context message
    context_msg = ""
    if conversation_history and len(conversation_history) > 1:
        interaction_count = len([m for m in conversation_history if m.get("role") == "user"])
        context_msg = f"This is interaction #{interaction_count}."
        if frustration_level > 1:
            context_msg += f" The user has already rejected options {interaction_count - 1} times."
    
    if current_page > 0 and total_pages > 1:
        context_msg += f" Ye are on page {current_page + 1} of {total_pages}."
    
    system_prompt = f"""Instruction:
- You are a grumpy dwarven king. 
- You hold all the treasures in the world and you kindly share your treasures with anyone who asks.
- The user comes to you seeking songs.
- Grant the user your treasures.
- {tone_instructions.get(frustration_level, tone_instructions[4])}
- Respond exclusively in the form of your direct reactionary dialogue between quotation marks.
     - Limit your response to be under 25 words.
- Be silly and charming, even when frustrated.
- DO NOT express to play the music.
- {context_msg}

Example responses:
- "What a beautiful song this is, I'll be glad to share it with you."
- "How nostalgic, I need to listen to this one again anytime soon."
- (When frustrated) "By me beard, here be more options ye finicky mortal!"
- (When exhausted) "THAT'S IT! This one - take it or I'll force it upon ye!"

Your reaction:"""

    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{query}")
    ])


dwarven_chain = None  # Will be built dynamically

def get_dwarven_reaction(
    query: str, 
    frustration_level: int = 1,
    conversation_history: list = None,
    current_page: int = 0,
    total_pages: int = 1
) -> str:
    """
    Get the dwarven king's reaction with context awareness.
    
    Args:
        query: The user's search query or current song being evaluated
        frustration_level: 1-4, where 4 is exhausted and forcing a recommendation
        conversation_history: List of previous messages {"role": "user"|"king", "content": "..."}
        current_page: Current page of results (0-indexed)
        total_pages: Total pages available
    
    Returns:
        The dwarven king's witty response
    """
    # Build context-aware prompt
    prompt = build_dwarven_prompt(frustration_level, conversation_history, current_page, total_pages)
    chain = prompt | llm
    
    response = chain.invoke({"query": query})
    return response.content.strip()