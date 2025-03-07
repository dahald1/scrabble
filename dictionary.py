def load_dictionary(filename):
    dictionary = set()
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()
            dictionary.add(word)
    return dictionary

def is_valid_word(word, dictionary):
    return word.lower() in dictionary

# We could declare the dictionary set as a global variable if needed.
filename = "dictionary.csv"
dictionary = load_dictionary(filename)

#print(is_valid_word("apple", dictionary))
#print(is_valid_word("aaaaa", dictionary))