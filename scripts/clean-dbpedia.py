from urllib.parse import urlparse
import json
import sys

### FUNCTIONS

# filter
def valid_triples(triple):
    assert isinstance(triple, tuple)
    assert len(triple) == 3
    subject, relation, obj = triple
    output = all([
        from_dbpedia(triple),
        not wiki_page_wiki_link(triple),
        not wiki_page_uses_template(triple),
        not has_file(triple),
        not has_template(triple)
        ])

    return output

def has_relation(triple, path):
    _, rel, _ = triple
    rel_parse = urlparse(rel)
    output = rel_parse.path.strip('/') == path.strip('/')
    return output

def has_keyword(uri, keyword):
    uri_parse = urlparse(uri)
    output = keyword in uri_parse.path
    return output

def has_file(triple):
    subj, rel, obj = triple
    kw = 'File:'
    output = any([
        has_keyword(subj, kw),
        has_keyword(rel, kw),
        has_keyword(obj, kw)
        ])
    return output

def has_template(triple):
    subj, rel, obj = triple
    kw = 'Template:'
    output = any([
        has_keyword(subj, kw),
        has_keyword(rel, kw),
        has_keyword(obj, kw)
        ])
    return output

def wiki_page_wiki_link(triple):
    return has_relation(triple, 'ontology/wikiPageWikiLink')

def wiki_page_uses_template(triple):
    return has_relation(triple, 'property/wikiPageUsesTemplate')

def from_dbpedia(triple):
    subj, rel, obj = triple
    output = all([is_dbpedia_uri(subj), is_dbpedia_uri(rel), is_dbpedia_uri(obj)])
    return output

def is_dbpedia_uri(uri):
    uri_parse = urlparse(uri)
    output = uri_parse.netloc == 'dbpedia.org'
    return output

def remap_triple(triple):
    triple = map(remap_uri, triple)
    return tuple(triple)

def remap_uri(uri):
    # take last part of uri
    uri_parse = urlparse(uri)
    output = uri_parse.path.split('/')[-1]
    output = '<' + output + '>'
    return output

### UNIT TESTS
def test_wiki_page_wiki_link():
    return wiki_page_wiki_link(('http://dbpedia.org/resource/Ada_Lovelace', 'http://dbpedia.org/ontology/wikiPageWikiLink', 'http://dbpedia.org/resource/Ron_Wyden'))

def test_has_relation():
    triple = ('http://dbpedia.org/resource/Ada_Lovelace', 'http://dbpedia.org/ontology/wikiPageWikiLink', 'http://dbpedia.org/resource/Ron_Wyden')
    return has_relation(triple, 'ontology/wikiPageWikiLink')

### RUN UNIT TESTS
assert test_has_relation()
assert test_wiki_page_wiki_link()

### MAIN
input_file = sys.argv[1]
output_file = sys.argv[2]

raw_data = json.load(open(input_file, 'r'))
triples = []
for x in raw_data:
    subject = x.get('subject').get('value')
    assert subject is not None
    relation = x.get('relation').get('value')
    assert relation is not None
    obj = x.get('object').get('value')
    assert obj is not None
    triples.append((subject, relation, obj))

triples = filter(valid_triples, triples)
triples = map(remap_triple, triples)
triples = sorted(set(triples))

with open(output_file, 'w') as f:
    f.write('\n'.join(' '.join(triple) for triple in triples) + '\n')
