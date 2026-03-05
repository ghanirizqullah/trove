from services.dwarven_agent import get_dwarven_reaction

# Test the agent
user_input = input("Enter text: ")
# king"I want to download Metallica - Enter Sandman"
response = get_dwarven_reaction(user_input)
print(f"User: {user_input}")
print(f"Dwarven King: {response}")