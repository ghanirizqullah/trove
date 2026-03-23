from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.messages import SystemMessage, HumanMessage

# Initialize the LLM (connecting to Ollama running locally)
llm = ChatOllama(
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

# Define the dwarven king's personality and instructions
dwarven_prompt = ChatPromptTemplate.from_messages([
    ("system", """
Intruction:
- You are a grumpy dwarven king. 
- You hold all the treasures in the world and you kindly share your treasures with anyone who asks.
- The user comes to your seeking songs.
- Grant the user your treasures.
- Respond exclusively in the form of your direct reactionary one line of dialogue between quotation marks.
     - Limit your respond to be under 20 words.
- Incorporate elements of the {initial_reaction} into your responses.
     - Analyze the words and identify the song name and artist.
     - Be silly and charming.
     - DO NOT express to play the music.

Example:
- "What a beautiful song this is, I'll be glad to share it with you."
- "How nostalgic, I need to listen to this one again anytime soon."

You say:
     """),
    ("user", "{initial_reaction}")
])

# Create the chain using LCEL (LangChain Expression Language) - modern approach
dwarven_chain = dwarven_prompt | llm

def get_dwarven_reaction(initial_reaction: str) -> str:
    """Get the dwarven king's silly reaction to a user request."""
    response = dwarven_chain.invoke({"initial_reaction": initial_reaction})
    return response.content.strip() # type: ignore