"""Test Vocab for UT
"""
import random
import re
import json
import time
#import requests

SAVEFILE = "KDATA"

def word_merge(old_data, new_data):
    """Returns a merged version of the old and new data."""
    if new_data['definitions'] == old_data['definitions']:
        # New metadata overwrites old metadata always.
        return new_data
    else:
        do_merge = input("Adding to existing definitions {0}? "
                         "[Y/n]".format(str(old_data['definitions'])))
        if do_merge:
            new_data['definitions'] += old_data['definitions']
            return new_data
        else:
            old_data['metadata'] = new_data['metadata']
            return old_data

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
    word = input("New word: ")
    if not word:
        return False
    # For textbook
    chapter = input("Chapter: ")
    # Textbook definitions
    definitions = re.split(r'\s*,+\s*', input("Definition (csv): "))
    return {'term': word, 'data': {'definitions': [definitions],
                                   'metadata': {'chapter': chapter}}}

def update_vocab():
    """Update vocab from console input."""
    vocab = fetch_vocab()
    while True:
        new_term = input_vocab()
        if new_term:
            # Merge the new word into the current data.
            word = new_term['term']
            if word in vocab.keys():
                print("\"{0}\" already found,"
                      "merging.".format(new_term['term']))
                vocab[word]['data'] = word_merge(vocab[word], new_term['data'])
            else:
                vocab[word] = {'data': new_term['data']}
        else:
            # No input signifies termination.
            # Save new data.
            break
    save_vocab(vocab, SAVEFILE)
    print("{0} vocabulary words saved.".format(len(vocab)))

def test_term(term, definition, vocab, def_filter=lambda _: True):
    """Score user input of a term for a given definition."""
    definition = [_ for _ in definition if def_filter(_)]
    query_string = ', '.join() + " = "

    score = 0
    user_in = input(query_string)
    if term == user_in:
        score = 1
    else:
        try:
            # Get list of definitions user specified
            alt_defs = vocab[user_in]['definitions']
        except KeyError:
            print('Answer was: {0}'.format(term))
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
def test_kor(user, term_filter=lambda _: True):
    """Test vocab using tags, querying keys."""
    vocab = fetch_vocab()
    terms = [term for term, data in vocab.items() if term_filter(term, data)]
    _vocab = json.dumps(vocab, sort_keys=True, indent=4,
                        separators=(',', ': '))
    print(_vocab)
    return

    random.shuffle(terms)
    terms = dict(terms)
    print(terms)
    scores = []
    start_time = time.time()


    # Generate useful feedback
    time_spent = int(time.time() - start_time)
    time_spent = (int(time_spent/60), time_spent%60)
    print("Spent %d minutes, %d seconds." % time_spent)
    for term, score in sorted(scores, key=lambda x: x[1]):
        if score > 0:
            print("%s; %s (%d tries)" % (term,
                                         ', '.join(vocab[term]['tags']),
                                         score))
        elif score == -1:
            print("FAILED on: %s; %s" % (term,
                                         ', '.join(vocab[term]['tags'])))
    return {user: scores}

#if __name__ == "__main__":
#    mode = int(input("Select mode (1, 2, 3): "))
#    if mode == 1:
#        update_vocab()
#    else:
#        test_kor(user=input("username="),
#                 word_filter=lambda term, data:
#                             data['metadata']['chapter'] == '-8')

if __name__ == "__main__":
    test_kor("Joshua Dong")
