# SCRABBLE CATS™ BANTER ®
# © 2025 P. Meiklem, E. Rigby, M. Mumthaz, D. Tomlinson

# WORD_CHECK.PY
# Checks words are valid Scrabble words
# Provides a score based on similarity to "Cat"

# REQUIRES closeness.json in same directory

import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
f = open(dir_path+"/closeness.json", "r")
dictionary = json.load(f)
f.close()

print("length is",len(dictionary))

def check_word_valid(word):
    return (word.lower() in dictionary)

#Returns 0 if word isn't in dictionary, or has no similarity to "cat"
def find_cat_similarity(word):
    try:
        return dictionary[word.lower()]
    except:
        return 0
