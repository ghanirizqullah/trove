import random

def get_initial_reaction(search_term):
    search_term = search_term
    reactions = [
        f'"{search_term}", eh?',
        f'"{search_term}" you say?',
        f'"{search_term}"... interesting...',
        f'How nostalgic. "{search_term}"',
        f'Whoa I wasn\'t expecting "{search_term}"'
    ]
    return reactions[random.randint(0,len(reactions)-1)]
