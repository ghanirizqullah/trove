from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.messages import SystemMessage, HumanMessage

# Initialize the LLM (connecting to Ollama running locally)
llm = ChatOllama(
    model="smollm2:360m",
    # model="tinyllama",
    # model="smollm2:135m",
    temperature=0.55,      # Balanced
    top_p=0.9,
    num_predict=90
    # reasoning=True
)

# Define the dwarven king's personality and instructions
dwarven_prompt = ChatPromptTemplate.from_messages([
    ("system", """
    Instruction:
    1. You are now fully embodying a gruff but charming king who grants song requests. 
    2. You are given your initial reaction towards a song request by the user.
    3. Within 20 words or less, continue your reaction in the form of dialogue in quotation marks without descriptors.
    4. Grant the request with scrutiny.
     
    Example:
    1. "I guess you can have it, here your go."
     

    Your dialogue:
     """),
    ("user", "{initial_reaction}")
    # 4. Use ** for non-dialogue descriptors.
    
    # Instructions:
    # 1. Scrutinize {user_request} into your dialogue.
    # 2. Within 20 words or less, respond in the form of dialogue in quotation marks of you granting the request without descriptors.
    # 3. Limit yourself to 1 line of dialogue. 
    # 4. ALWAYS respond positively to the request.
    # 5. Do not ask questions.

    # Your dialogue:
    
    # ("system", """
    # You are now fully embodying a gruff but charming king who grants song requests. The user will provide you queries which can be a combination of song name and artist.
     
    # Instructions:
    # 1. Incorporate the elements of the {user_request} into your dialogue.
    # 2. Within 20 words or less, respond in the form of dialogue in quotation marks of you granting the request without descriptors.
    # 3. Limit yourself to 1 line of dialogue. 
    # 4. ALWAYS respond positively to the request.
    # 5. Do not ask questions.

    # Your dialogue:
    #  """),
    # ("user", "I seek {user_request}")
])

# Create the chain using LCEL (LangChain Expression Language) - modern approach
dwarven_chain = dwarven_prompt | llm

def get_dwarven_reaction(initial_reaction: str) -> str:
    """Get the dwarven king's silly reaction to a user request."""
    response = dwarven_chain.invoke({"initial_reaction": initial_reaction})
    return response.content.strip() # type: ignore