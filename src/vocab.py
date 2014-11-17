"""Handler for vocab data saves and updating."""
import json
import parse_raw

SAVEPATH = "../data/"
SAVEFILE = "vocab.json"

def fetch_json(filepath=SAVEPATH+SAVEFILE):
    """Fetch data from filepath, if it exists."""
    try:
        with open(filepath, 'r') as fptr:
            return json.load(fptr)
    except IOError:
        # In case of no file, use an empty JSON element.
        return {}

def save_json(data, filepath=SAVEPATH+SAVEFILE):
    """Save json as JSON."""
    with open(filepath, 'w') as fptr:
        fptr.write(json.dumps(data, sort_keys=True, indent=2,
                              separators=(',', ': ')))

def merge_definitions(arr1, arr2):
    return arr1 + arr2

def merge_entry(new_data, vocabulary):
    """Merges new_data into vocabulary."""
    keys = new_data.keys()
    for key in keys:
        if key not in vocabulary.keys():
            vocabulary[key] = new_data[key]
        else:
            old_entry = vocabulary[key]
            # Merge definitions.
            old_entry['data']['definitions'] =\
                    merge_definitions(old_entry['data']['definitions'],
                                      new_data[key]['data']['definitions'])
            # Always overwrite old metadata.
            old_entry['data']['metadata'] = new_data[key]['data']['metadata']
            # Update vocabulary
            vocabulary[key] = old_entry

def vocab_to_json(file_in="../data/RAW.txt", file_out="../data/raw.json"):
    """Parse raw data into json."""
    save_json(parse_raw.parse_file(file_in), filepath=file_out)

def merge_from_array(file_in, vocab_out=SAVEPATH+SAVEFILE):
    """Merge elements from a JSON array at file_in into a vocabulary at
    file_out.
    """
    from pprint import pprint
    vocabulary = fetch_json(vocab_out)
    print("Merging from {}.".format(file_in))
    for entry in fetch_json(file_in):
        key = entry['term']
        chapter = entry['section']['chapter']
        section = entry['section']['part']
        definitions = entry['definitions']
        grammar_classes = entry['class']
        vocab_entry = {
            key: {
                "data": {
                    "definitions": [definitions],
                    "metadata": {
                        "chapter": chapter,
                        "section": section,
                        "classes": grammar_classes,
                    }
                }
            }
        }
        merge_entry(vocab_entry, vocabulary)
    save_json(vocabulary)

if __name__ == "__main__":
    vocab_to_json()
    merge_from_array("../data/raw.json")
