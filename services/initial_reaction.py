import random

def get_initial_reaction(search_term):
    search_term = search_term
    reactions = [
        f'"{search_term}", eh?',
        f'"{search_term}" you say?',
        f'"{search_term}"... interesting...',
        f'I see... It has been awhile since "{search_term}" was sought.'
    ]
    return reactions[random.randint(0,len(reactions)-1)]
