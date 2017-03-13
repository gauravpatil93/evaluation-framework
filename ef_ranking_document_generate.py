import argparse
from copy import deepcopy

import tagme
from trec_car.format_runs import *
from trec_car.read_data import *

from ef_BM25_ranking import *

GCUBE_TOKEN = "bfbfb535-3683-47c0-bd11-df06d5d96726-843339462"

parser = argparse.ArgumentParser()
parser.add_argument("outline_file", type=str, help="Qualified location of the outline file")
parser.add_argument("paragraph_file", type=str, help="Qualified location of the paragraph file")
parser.add_argument("output_file", type=str, help="Name of the output file")
parser.add_argument("use_enchanced_query", type=str, help="Use tageme enchanced queries")
args = vars(parser.parse_args())

query_cbor = args['outline_file']
paragraphs_cbor = args['paragraph_file']
output_file_name = args['output_file']
use_enchanced_query = args['use_enchanced_query']

if use_enchanced_query == "enhanced" or use_enchanced_query == "notenhanced":
    pass
else:
    exit()

# Pages
pages = []
with open(query_cbor, 'rb') as f:
    for p in itertools.islice(iter_annotations(f), 0, 1000):
        pages.append(p)
    print("Gathered Pages")

# Paragraphs
paragraphs = []
with open(paragraphs_cbor, 'rb') as f:
    for p in itertools.islice(iter_paragraphs(f), 0, 500, 5):
        para_id = p.para_id
        para_content = p.get_text().lower().replace(',', '').replace('.', '')
        para_content_list_of_words = para_content.split()
        para_length = len(para_content_list_of_words)
        tup = (para_id, para_length, para_content, para_content_list_of_words)
        paragraphs.append(tup)
    print("Gathered Paragraphs")

queries = []
if use_enchanced_query == "enhanced":
    print("Generating TagMe enchanced queries")
    # Generate tageme queries
    for page in pages:
        for section_path in page.flat_headings_list():
            query_id_plain = " ".join([page.page_name] + [section.heading for section in section_path])
            query_id_formatted = "/".join([page.page_id] + [section.headingId for section in section_path])
            enchance_query_list = query_id_plain.split()
            annotations = tagme.annotate(query_id_plain, GCUBE_TOKEN)
            for annotation in annotations.get_annotations(0.1):
                enchance_query_list += annotation.entity_title.replace('(', '').replace(')', '').split()
            tup = (query_id_plain.lower(), query_id_formatted, list(set(enchance_query_list)))
            print(tup)
            queries.append(tup)
    print("Gathered Tagme Enhanced Queries")
if use_enchanced_query == "notenhanced":
    # Generate queries in plain text
    for page in pages:
        for section_path in page.flat_headings_list():
            query_id_plain = " ".join([page.page_name] + [section.heading for section in section_path])
            query_id_formatted = "/".join([page.page_id] + [section.headingId for section in section_path])
            tup = (query_id_plain.lower(), query_id_formatted, query_id_plain.split())
            queries.append(tup)
    print("Gathered Regular Queries")

bm25_instance = BM25(queries, paragraphs)

# Generate the query scores
query_scores = dict()
for query in queries:
    temp_list = []
    for document in paragraphs:
        temp_list.append(bm25_instance.bm25_score(query, document))
    temp_list.sort(key=lambda m: m[2])
    temp_list.reverse()
    query_scores[query[0]] = deepcopy(temp_list)

# Write the results to a file
with open(output_file_name, mode='w', encoding='UTF-8') as f:
    writer = f
    temp_list = []
    count = 0
    for key, value in query_scores.items():
        count += 1
        rank = 0
        for x in value:
            rank += 1
            temp_list.append(RankingEntry(x[0], x[1], rank, x[2]))
    format_run(writer, temp_list, exp_name='test')
    print("Gathered Results")
    f.close()
