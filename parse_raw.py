"""Parse human data into JSON"""
import string
from pprint import pprint

def parse_file(filename="RAW.txt"):
    """Parse human readable file into JSON."""

    entries = []
    with open(filename) as f_in:
        next_line = f_in.readline()
        data = {}
        state = "section"
        while next_line:
            if state == "section":
                line = next_line.split(" ")
                if line[0] == "Chapter":
                    data = {'section': {'chapter': int(line[1]),
                                        'part': line[4].strip()}}
                    state = "term"
            elif state == "term":
                if not next_line.strip():
                    state = "section"
                    next_line = f_in.readline()
                    continue
                entry = data.copy()
                term, definition = next_line.split(";")
                print("'{}'".format(next_line))
                exit()

                entry['term'] = term.strip()
                entry['definitions'] = [_.strip() for\
                                        _ in definition.split(",")]
                entry['class'] = []

                # Determine the lexical class of the word.
                if "(be)" in "".join(entry['definitions']):
                    entry['class'].append("adjective")
                for _ in entry['definitions']:
                    initial = _.split(" ")[0]
                    end = _[-1]
                    if initial in ["a", "an"]:
                        entry['class'].append("noun")
                    if initial in ["to"]:
                        entry['class'].append("verb")
                    if end in ".!?":
                        entry['class'].append("phrase")
                    # Proper nouns
                    elif initial[0] in string.ascii_uppercase:
                        entry['class'].append("noun")
                entries.append(entry)
            next_line = f_in.readline()
    return entries
