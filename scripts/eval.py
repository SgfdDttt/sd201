import sys
import json
import argparse
import math

def canonicalize_triple(triple):
    assert isinstance(triple, tuple), triple
    assert len(triple) == 3
    output = tuple(map(canonicalize_string, triple))
    return output

def canonicalize_string(string):
    assert valid_kbe(string), string
    output = string[1:-1]
    output = output.lower().replace('_','').replace(' ','')
    return output

def valid_kbe(string):
    if not isinstance(string, str):
        return False
    if len(string) < 2:
        return False
    c1 = string[0] == '<'
    c2 = string[-1] == '>'
    return c1 and c2

def parse_triple(string):
    # this is the converse of triple_to_string
    assert isinstance(string, str), string
    triple = tuple(string.split())
    assert len(triple) == 3, triple
    return triple

def triple_to_string(triple):
    # this is the converse of parse_triple
    assert isinstance(triple, tuple)
    assert len(triple) == 3
    output = ' '.join(triple)
    assert isinstance(output, str)
    return output

def correct(prediction, reference):
    assert isinstance(prediction, set)
    assert isinstance(reference, set)
    return set(prediction & reference)

def num_correct(prediction, reference):
    return len(correct(prediction, reference))

def overlap_function(a,b):
    assert isinstance(a, set)
    assert isinstance(b, set)
    if len(a) == 0:
        output = 1
    else:
        n = len(a & b)
        output = n/len(a)
    return output

def precision(prediction, reference):
    return overlap_function(prediction, reference)

def recall(prediction, reference):
    return overlap_function(reference, prediction)

def fscore(prediction, reference):
    assert isinstance(prediction, set)
    assert isinstance(reference, set)
    n = len(prediction & reference)
    p = len(prediction)
    r = len(reference)
    if p+r == 0:
        output = 1.
    else:
        output = 2*n/(p + r)
    return output

def alignment_matrix(prediction, reference):
    output = {}
    for pred in prediction:
        for ref in reference:
            key = (pred, ref)
            assert key not in output
            output[key] = triple_similarity(pred, ref)
        # end for ref in reference:
    # end for pred in prediction:
    return output

def triple_similarity(triple1, triple2):
    for t in [triple1, triple2]:
        assert isinstance(t, tuple)
        assert len(t) == 3
    similarities = [string_similarity(x,y) for x,y in zip(triple1, triple2)]
    output = [math.log(x) if x>0 else -float('inf') for x in similarities]
    output = sum(output)/3
    output = math.exp(output)
    return output

def string_similarity(s1, s2):
    assert isinstance(s1, str)
    assert isinstance(s2, str)
    cs1 = canonicalize_string(s1)
    cs2 = canonicalize_string(s2)
    output = edit_distance(cs1, cs2)
    S = max(len(cs1), len(cs2))
    normalized_distance = output/S
    return 1-normalized_distance

def edit_distance(s1, s2):
    assert isinstance(s1, str)
    assert isinstance(s2, str)
    l1 = len(s1)
    l2 = len(s2)
    cache = [[None for _ in range(1+l2)] for _ in range(1+l1)]
    for ii in range(1+l1):
        for jj in range(1+l2):
            if jj == 0:
                cache[ii][jj] = ii
            elif ii == 0:
                cache[ii][jj] = jj
            else:
                deletion = 1+cache[ii][jj-1]
                insertion = 1+cache[ii-1][jj]
                substitution = cache[ii-1][jj-1] if s1[ii-1] == s2[jj-1] else 1+cache[ii-1][jj-1]
                cache[ii][jj] = min([deletion, insertion, substitution])
            # end if jj == 0:
        # end for jj,c2 in enumerate(s2):
    # end for ii,c1 in enumerate(s1):
    output = cache[l1][l2]
    return output

def max_alignment_sum(alignment, index):
    # this computes maximum over row or column in a matrix,
    # and returns the number of rows or columns
    assert index in range(2)
    max_per_key = {}
    alignment_args = {}
    for pair, value in alignment.items():
        key = pair[index]
        max_per_key.setdefault(key, -float('inf'))
        alignment_args.setdefault(key, None)
        if max_per_key[key] < value:
            alignment_args[key] = pair[1-index]
            max_per_key[key] = value
        # end if max_per_key[key] < value:
    # end for pair, value in alignment.items():
    output = sum(v for _,v in max_per_key.items())
    return output, alignment_args

def soft_precision(alignment):
    # the alignment matrix's keys are (predicted, reference)
    # so soft precision is sum of predicted's alignment
    S, alignment_args = max_alignment_sum(alignment, 0)
    output = S/len(alignment_args.keys())
    return output, alignment_args

def soft_recall(alignment):
    # the alignment matrix's keys are (predicted, reference)
    # so soft recall is sum of reference's alignment
    S, alignment_args = max_alignment_sum(alignment, 1)
    output = S/len(alignment_args.keys())
    return output, alignment_args

def soft_fscore(soft_recall, soft_precision):
    if (soft_recall == 0.) or (soft_precision == 0.):
        return 0.
    else:
        return 2*soft_recall*soft_precision/(soft_recall + soft_precision)

def format_number(number):
    output = 100*number # to percentage
    output = round(output, args.significant)
    return '{}%'.format(output)

def format_alignment_matrix(alignment):
    output = {}
    for key, value in alignment.items():
        output[triple_to_string(key)] = triple_to_string(value)
    return output

def alignment_to_string(alignment):
    output = format_alignment_matrix(alignment)
    output = json.dumps(output, sort_keys=True, indent=2)
    assert isinstance(output, str)
    return output

# UNIT TESTS
assert edit_distance("cat","cat") == 0
assert edit_distance("cat","dog") == 3
assert edit_distance("dog","cat") == 3
assert edit_distance("dog","cat") == 3
def test_recall():
    prediction = set(("a","b","d"))
    reference = set(("a","b","c"))
    r = recall(prediction, reference)
    return r == 2/3
def test_precision():
    prediction = set(("a","b","d","e"))
    reference = set(("a","b","c"))
    r = precision(prediction, reference)
    return r == 2/4
def test_canonicalization1():
    return canonicalize_string("<knownFor>") == "knownfor"
def test_canonicalization2():
    return canonicalize_string("<Ada_Lovelace>") == "adalovelace"
assert test_recall()
assert test_precision()
assert test_canonicalization1()
assert test_canonicalization2()

### MAIN
parser = argparse.ArgumentParser(description="Knowledge graph evaluator")
parser.add_argument(
    '--reference',
    required=True,
    type=argparse.FileType('r'),
    help=('Reference file containing the gold knowledge graph.')
    )
parser.add_argument(
    '--prediction',
    required=True,
    type=argparse.FileType('r'),
    help=('File containing the predicted knowledge graph.')
    )
parser.add_argument(
    '--significant',
    type=int,
    default=1,
    help='significant digits to output (default: 2)')
parser.add_argument(
    '--alignment',
    action='store_true',
    help='whether to print out the alignment between prediction and reference')

args = parser.parse_args()

reference_triples = set(map(parse_triple, args.reference))
predicted_triples = set(map(parse_triple, args.prediction))

# compute metrics
alignment = alignment_matrix(predicted_triples, reference_triples)
sp, pargs = soft_precision(alignment)
sr, rargs = soft_recall(alignment)
metrics = {
        'exact match': {
            'precision': precision(predicted_triples, reference_triples),
            'recall': recall(predicted_triples, reference_triples),
            'fscore': fscore(predicted_triples, reference_triples)
            },
        'soft match': {
            'precision': sp,
            'recall': sr,
            'fscore': soft_fscore(sp,sr)
            }
        }
# format and print metrics
for major_key in metrics:
    for minor_key, value in metrics[major_key].items():
        metrics[major_key][minor_key] = format_number(value) if isinstance(value, float) else value
print(json.dumps(metrics, sort_keys=True, indent=2))

# optionally print alignment
if args.alignment:
    print('alignment soft precision'.upper())
    print('"<prediction>": "<reference>"')
    print(alignment_to_string(pargs))
    print('alignment soft recall'.upper())
    print('"<reference>": "<prediction>"')
    print(alignment_to_string(rargs))

"""for x, y in [
        ("<Ada_Lovelace> <child> <Anne_Blunt,_15th_Baroness_Wentworth>","<Lovelace> <child> <Anne_Blunt,_15th_Baroness_Wentworth>"),
        ("<Ada_Lovelace> <child> <Ralph_King-Milbanke,_2nd_Earl_of_Lovelace>", "<Lady_Lovelace> <child> <Ralph_King-Milbanke>"),
        ("<Ada_Lovelace> <spouse> <William_King-Noel,_1st_Earl_of_Lovelace>", "<Ada_Lovelace> <married> <William_King-Noel,_1st_Earl_of_Lovelace>")
        ]:
    print(x,y)
    print(triple_similarity(parse_triple(x),parse_triple(y)))"""
