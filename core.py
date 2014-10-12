"""CLI vocab input and basic tester.
"""
import random
import re
import json
import time
#import requests

SAVEFILE = "KDATA"

def word_merge(old_data, new_data):
    """Returns a merged version of the old and new data."""
    merge_data = []
    if new_data['definitions'][0] in old_data['definitions']:
        # New metadata overwrites old metadata always.
        merge_data = new_data
    else:
        do_merge = input("Adding to existing definitions {0}? "
                         "[Y/n] ".format(str(old_data['definitions'])))
        if do_merge == "y" or not do_merge:
            merge_data = new_data
            merge_data.update({'definitions': new_data['definitions'] +\
                                              old_data['definitions']})
        else:
            merge_data = old_data
    return merge_data

def save_vocab(vocab, filename):
    """Save vocab as JSON."""
    with open(filename, 'w') as fptr:
        fptr.write(json.dumps(vocab, sort_keys=True, indent=4,
                              separators=(',', ': ')))

def fetch_vocab(filename=SAVEFILE):
    """Fetch data from filename, if it exists."""
    try:
        with open(filename, 'r') as fptr:
            return json.load(fptr)
    except IOError:
        # In case of no file, use an empty JSON element.
        return {}

#def input_vocab(lang='en'):

def input_vocab():
    """Receive new vocab word data from the user."""
    term_category = "term"
    word = input("New word: ")
    if not word:
        return False
    # For textbook
    chapter = input("Chapter: ")
    # Textbook definitions
    definitions = input("Definition (csv): ")
    if definitions == "":
        return -1
    definitions = re.split(r'\s*,+\s*', definitions)
    # Hardcoding particle handling
    if word[0] == "-" and "particle" in ' '.join(definitions):
        term_category = "particle"
    return {'term': word, 'data': {'definitions': [definitions],
                                   'metadata': {'chapter': chapter,
                                                'type': term_category}}}

def update_vocab():
    """Update vocab from console input."""
    vocab = fetch_vocab()
    while True:
        new_term = input_vocab()
        # Mistakes
        if new_term == -1:
            print("Skipped (no definition).")
            continue
        if new_term:
            # Merge the new word into the current data.
            word = new_term['term']
            if word in vocab.keys():
                print("\"{0}\" already found, "
                      "merging.".format(new_term['term']))
                vocab[word]['data'] = word_merge(vocab[word]['data'],
                                                 new_term['data'])
            else:
                vocab[word] = {'data': new_term['data']}
        else:
            # No input signifies termination.
            # Save new data.
            break
    save_vocab(vocab, SAVEFILE)
    print("{0} words in vocabulary.".format(len(vocab)))

def test_term(term, definition, vocab, def_filter=lambda _: True):
    """Score user input of a term for a given definition."""
    definition = [_ for _ in definition if def_filter(_)]
    query_string = ', '.join(definition) + " = "

    score = 0
    user_in = input(query_string)
    if term == user_in:
        score = 1
    else:
        try:
            # Get list of definitions user specified
            alt_defs = vocab[user_in]['definitions']
        except KeyError:
            alt_defs = []
            score = 0
        # handling "hash collisions"
        for alt_def in alt_defs:
            # Check for synonyms, only exact matches
            # No triple exact synonyms, pls.
            if set(alt_def) == set(definition):
                print('Find a synonym.')
                user_in = input(query_string)
                if term == user_in:
                    score = 1
                else:
                    score = 0
                break
        if score == 0:
            print('Answer was: {0}'.format(term))
    return score

# Add/implement a timing decorator.
def test_kor(term_filter=lambda a, b: True):
    """Test vocab using tags, querying keys."""
    vocab = fetch_vocab()
    terms = {term: data['data']['definitions'] for term, data in vocab.items()\
             if term_filter(term, data)}
    if not terms:
        return 0,0,0
    max_score = len(terms)
    score = 0
    misses = []
    test = [_ for _ in terms.items()]
    random.shuffle(test)
    for term, definition in test:
        result = test_term(term, random.choice(definition), vocab)
        score += result
        # 1 is a perfect score
        if result != 1:
            misses.append(term)
    return misses, score, max_score

#if __name__ == "__main__":
#    mode = int(input("Select mode (1, 2, 3): "))
#    if mode == 1:
#        update_vocab()
#    else:
#        test_kor(user=input("username="),
#                 word_filter=lambda term, data:
#                             data['metadata']['chapter'] == '-8')

def do_test(test_function):
    """Basic testing wrapper"""
    # Generate useful feedback
    start_time = time.time()

    misses, score, max_score = test_function()

    time_spent = int(time.time() - start_time)
    time_spent = (int(time_spent/60), time_spent%60)
    print("Spent %d minutes, %d seconds." % time_spent)

    for miss in misses:
        print("MISSED: {0}".format(miss))

    print("SCORE: {0}%".format(int(score*100/max_score)))


if __name__ == "__main__":
    update_vocab()
    if input("Do test? [N/y] ") == "y":
        do_test(test_kor)
