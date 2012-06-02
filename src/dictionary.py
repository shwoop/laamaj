#    Seperate module for querying a dictionary
#    Using NLTK and WordNet
from nltk.corpus import wordnet

def lookup_dictionary(check_word):
  # feed in a word and return a long string of definition
  #synsets = wordnet.synsets(check_word)
  #for synset in synsets:
  #  output = check_word + ": " + synset.definition
  #return output
  return wordnet.synsets(check_word)

#print (lookup_dictionary("space"))

