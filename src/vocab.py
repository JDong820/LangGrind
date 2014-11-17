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

def vocab_to_json(file_in="../data/RAW.txt", file_out="../data/raw.json"):
    """Parse raw data into json."""
    save_json(parse_raw.parse_file(file_in), filepath=file_out)
