import argparse

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

for x in paragraphs:
    print(bm25_instance.bm25_score(queries[0][0], x[0], x[3]))
