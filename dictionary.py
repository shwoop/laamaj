#    Seperate module for querying a dictionary
#    Using NLTK and WordNet
from nltk.corpus import wordnet

def lookup_dictionary(check_word)
  # feed in a word and return a long string of definition
  counter = 1
  output = ""
  synsets = wordnet.synsets(check_word)
  for synset in synsets:
      output = output + check_word + ": " + str(counter) + "* " + synset.definition + "\n"
      counter = counter + 1
  #print(output)
  return output

#print (lookup_dictionary("space"))

