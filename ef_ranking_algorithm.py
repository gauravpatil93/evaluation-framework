import argparse
from copy import deepcopy

from trec_car.format_runs import *
from trec_car.read_data import *

from ef_BM25_ranking import *

parser = argparse.ArgumentParser()
parser.add_argument("outline_file", type=str, help="Qualified location of the outline file")
parser.add_argument("paragraph_file", type=str, help="Qualified location of the paragraph file")
parser.add_argument("output_file", type=str, help="Name of the output file")
args = vars(parser.parse_args())

query_cbor = args['outline_file']
paragraphs_cbor = args['paragraph_file']
output_file_name = args['output_file']

pages = []
with open(query_cbor, 'rb') as f:
    for p in itertools.islice(iter_annotations(f), 0, 1000):
        pages.append(p)

paragraphs = []
with open(paragraphs_cbor, 'rb') as f:
    for p in itertools.islice(iter_paragraphs(f), 0, 500, 5):
        tup = (p.para_id, p, len(p.get_text().lower().replace(',', '').replace('.', '').split()),
               p.get_text().lower().replace(',', '').replace('.', ''))
        paragraphs.append(tup)

# Generate queries in plain text
queries = []
for page in pages:
    for section_path in page.flat_headings_list():
        query_id_plain = " ".join([page.page_name] + [section.heading for section in section_path])
        query_id_formatted = "/".join([page.page_id] + [section.headingId for section in section_path])
        tup = (query_id_plain, query_id_formatted)
        queries.append(tup)

bm25_instance = BM25(queries, paragraphs)

query_scores = dict()
for query in queries:
    temp_list = []
    for document in paragraphs:
        temp_list.append(bm25_instance.bm25_score(query, document[0], document[3]))
    temp_list.sort(key=lambda x: x[3])
    temp_list.reverse()
    query_scores[query] = deepcopy(temp_list)

with open(output_file_name, mode='w', encoding='UTF-8') as f:
    writer = f
    temp_list = []
    for key, value in query_scores.items():
        rank = 0
        for x in value:
            rank += 1
            temp_list.append(RankingEntry(x[0], x[2], rank, x[3]))
    format_run(writer, temp_list, exp_name='test')
    f.close()
