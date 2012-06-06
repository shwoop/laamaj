#    Seperate module for querying a dictionary
#    Using NLTK and WordNet
from nltk.corpus import wordnet

def lookup_synset(check_word):
    # Return the whole synset from wordnet
    return wordnet.synsets(check_word)

def lookup_definition(check_word):
    # extract and return list of definitions from wordnet
    synsets = wordnet.synsets(check_word)
    definitions = []
    
    for synset in synsets:
        definitions.append(synset.definition)
    
    return definitions

