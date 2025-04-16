# SCRABBLE CATS™ BANTER ®
# © 2025 P. Meiklem, E. Rigby, M. Mumthaz, D. Tomlinson

# RULES.PY
# Generates Scrabble Banter-Style rules
# Checks words follow rules

# REQUIRES words.txt in operating directory

# Usage guide:
# Initiate rule with Rule()
# EITHER:
#     Create from parameters with create_rule(type1, letters1, type2, letters2)
#     OR Generate randomly with generate_rule(difficulty)
# Check words with rule.check_word()
# Export rule to tuple with rule.to_tuple()

import random
import numpy as np

letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
           "w", "x", "y", "z"]
rules_str = ["Starts with", "Must have", "Can't have", "Ends in"]


def get_words():
    f = open("Rules/words.txt", "r")
    s = f.read().lower()
    return s.split("\n")


scrabble_words = get_words()
scrabble_word_count = len(scrabble_words)


def random_letters():
    num = random.randint(1, 4)
    if (num == 1):
        return (letters[random.randint(0, 25)] + letters[random.randint(0, 25)])
    else:
        return letters[random.randint(0, 25)]


def check_single_rule(word, rule_type, rule_letters):
    if (rule_type == 0):
        return word.startswith(rule_letters)
    elif (rule_type == 1):
        return (word.count(rule_letters) > 0)
    elif (rule_type == 2):
        return (word.count(rule_letters) == 0)
    elif (rule_type == 3):
        return word.endswith(rule_letters)


def create_rule(type1, letters1, type2, letters2):
    rule = Rule()
    rule.set(type1, letters1, type2, letters2)
    return rule


def generate_rule(difficulty):
    rule = Rule()
    rule.generate(difficulty)
    return rule


class Rule:

    def __init__(self):
        self.rule_1_type = 0
        self.rule_2_type = 0
        self.rule_1_letters = "a"
        self.rule_2_letters = "a"

    def __str__(self):
        return (rules_str[self.rule_1_type] + " \"" + self.rule_1_letters.upper() + "\", " +
                rules_str[self.rule_2_type] + " \"" + self.rule_2_letters.upper() + "\"")
    def set(self, rule_1_type, rule_1_letters, rule_2_type, rule_2_letters):
        self.rule_1_type = rule_1_type
        self.rule_1_letters = rule_1_letters.lower()
        self.rule_2_type = rule_2_type
        self.rule_2_letters = rule_2_letters.lower()

    def to_tuple(self):
        return (self.rule_1_type, self.rule_1_letters, self.rule_2_type, self.rule_2_letters)

    # Gives this "Rule" object a random pair of word rules
    def generate_random(self):
        num = random.randint(1, 6)
        if (num == 1):
            self.rule_1_type = 0
            self.rule_2_type = 1
        elif (num == 2):
            self.rule_1_type = 0
            self.rule_2_type = 2
        elif (num == 3):
            self.rule_1_type = 0
            self.rule_2_type = 3
        elif (num == 4):
            self.rule_1_type = 1
            self.rule_2_type = 2
        elif (num == 5):
            self.rule_1_type = 1
            self.rule_2_type = 3
        elif (num == 6):
            self.rule_1_type = 2
            self.rule_2_type = 3
        self.rule_1_letters = random_letters()
        self.rule_2_letters = random_letters()

    def check_word(self, word):
        word = word.lower()
        return (check_single_rule(word, self.rule_1_type, self.rule_1_letters) and check_single_rule(word,
                                                                                                     self.rule_2_type,
                                                                                                     self.rule_2_letters))

    def check_word_2(self, word):
        word = word.lower()
        return (check_single_rule(word, self.rule_1_type, self.rule_1_letters),
                check_single_rule(word, self.rule_2_type, self.rule_2_letters))

    def evaluate_difficulty(self):
        counts = np.zeros(4)  # Neither, First, Second, Both
        for word in scrabble_words:
            result = self.check_word_2(word)
            if (result[0] and result[1]):
                counts[3] += 1
            else:
                if (result[0]):
                    counts[1] += 1
                elif (result[1]):
                    counts[2] += 1
                else:
                    counts[0] += 1
        frequencies = counts * 100 / scrabble_word_count
        return frequencies

    def is_reasonable(self, difficulty):
        frequencies = self.evaluate_difficulty()
        min_freq = 1 / difficulty
        max_freq = 40 / difficulty
        if (frequencies[1] > 0.00001 and frequencies[1] < 50 and frequencies[2] > 0.00001 and frequencies[2] < 50 and
                frequencies[3] > min_freq and frequencies[3] < max_freq):
            return True
        return False

    def generate(self, difficulty):
        rule_valid = False
        while (not rule_valid):
            self.generate_random()
            if (self.is_reasonable(difficulty)):
                rule_valid = True



