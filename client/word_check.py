# SCRABBLE CATS™ BANTER ®
# © 2025 P. Meiklem, E. Rigby, M. Mumthaz, D. Tomlinson

# WORD_CHECK.PY
# Checks words are valid Scrabble words
# Provides a score based on similarity to "Cat"

# REQUIRES dictionary.json in operating directory

import json

f = open("dictionary.json", "r")
dictionary = json.load(f)
f.close()

def check_word_valid(word):
    return (word.lower() in dictionary)

#Returns 0 if word isn't in dictionary, or has no similarity to "cat"
def find_cat_similarity(word):
    try:
        return dictionary[word.lower()]
    except:
        return 0
