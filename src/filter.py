from jamo import jamo
import vocab

VOCAB = vocab.fetch_json()

def filter_ae():
    """Eventually turn this into a boolean filter function.
    """
    results = {}
    for key, item in VOCAB.items():
        for c in key:
            v = jamo.jamo_to_hcj(jamo.hangul_to_jamo(c)[1])
            if v in ["ㅔ", "ㅐ"]:
                results[key] = item
                break
    return results

def filter_ou():
    """Eventually turn this into a boolean filter function.
    """
    results = {}
    for key, item in VOCAB.items():
        for c in key:
            v = jamo.jamo_to_hcj(jamo.hangul_to_jamo(c)[1])
            if v in ["ㅗ", "ㅜ"]:
                results[key] = item
                break
    return results

def vprint(key, data):
    """Pretty print for vocab."""
    data = data['data']
    definitions = data['definitions']
    chapter = data['metadata']['chapter']
    #grammar_class = data['metadata']['class']

    try:
        definitions = '; '.join([', '.join(definition)\
                                 for definition in definitions])
    except TypeError:
        print(definitions)
        exit(0)

    print(("{key}: {definitions}\t"
           "(ch. {chapter})").format(key=key,
                                       chapter=chapter,
                                       definitions=definitions))

if __name__ == "__main__":
    items = list(filter_ou().items())
    for key, data in sorted(items,
            key=lambda _: _[1]['data']['metadata']['chapter']+
                          (0.5 if _[1]['data']['metadata']['section'] == "aux" else 0)):
        vprint(key, data)
