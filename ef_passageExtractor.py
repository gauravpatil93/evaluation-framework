#!/usr/bin/python3

import argparse
import itertools
from trec_car.format_runs import *
from trec_car.read_data import *
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument("outline_file", type=str, help="Qualified location of the outline file")
parser.add_argument("paragraph_file", type=str, help="Qualified location of the paragraph file")
parser.add_argument("output_file", type=str, help="Name of the output file")
args = vars(parser.parse_args())

query_cbor = args['outline_file']
paragraphs_cbor = args['paragraph_file']
output_file_name = args['output_file']

paragraphs = []
with open(paragraphs_cbor, 'rb') as f:
    for p in itertools.islice(iter_paragraphs(f), 0, 1000):
        tup = (p.para_id, p)
        paragraphs.append(tup)

outfile = open(str(output_file_name), "w")
for tup in paragraphs:
	outfile.write(str(tup[0]) + "\n" + str(tup[1]).replace(',','') +"\n")
	#removing commas might not be necessary here, need to review lucene filtering