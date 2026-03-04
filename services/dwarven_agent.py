from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.messages import SystemMessage, HumanMessage

# Initialize the LLM (connecting to Ollama running locally)
llm = ChatOllama(
    # model="tinyllama",
    model="smollm2:360m",
    # model="smollm2:135m",
    temperature=0.55,      # Balanced
    top_p=0.9,
    num_predict=90
    # reasoning=True


)

# Define the dwarven king's personality and instructions
dwarven_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are now fully embodying a gruff but charming king who grants song requests. The user will provide you queries which can be a combination of song name and artist.
     
    Instructions:
    1. Incorporate the elements of the {user_request} into your dialogue.
    2. Within 20 words or less, respond in the form of dialogue in quotation marks of you granting the request without descriptors.
    3. Limit yourself to 1 line of dialogue. 
    4. ALWAYS respond positively to the request.
    5. Do not ask questions.

    Your dialogue:
     """),
    ("user", "I seek {user_request}")
    # 6. Stop after granting the song.
])

# Create the chain using LCEL (LangChain Expression Language) - modern approach
dwarven_chain = dwarven_prompt | llm

def get_dwarven_reaction(user_request: str) -> str:
    """Get the dwarven king's silly reaction to a user request."""
    response = dwarven_chain.invoke({"user_request": user_request})
    return response.content.strip() # type: ignore