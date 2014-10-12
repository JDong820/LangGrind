"""Test Vocab for UT
"""
import random
import re
import pickle
import time
import requests
import core


if __name__ == "__main__":
    VOCAB = core.fetch_vocab()
    while True:
        tags = input("EN->KO: ")
        tags = re.split(r'\s*,+\s*', tags)
        results = []
        for term, data in VOCAB.items():
            missed_tag = False
            for tag in tags:
                if tag not in data['tags']:
                    missed_tag = True
                    break
            if missed_tag:
                continue
            results.append(term)
        print('{%s: %s}' % (tags, str(results)))
        try:
            print(VOCAB[input("KO->EN: ")]['tags'])
        except KeyError:
            pass

