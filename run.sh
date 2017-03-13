#!/bin/bash
echo "============================================================="
echo "Generating results file with regular queries................."
echo "============================================================="

python ef_ranking_document_generate.py spritzer.cbor.outlines spritzer.cbor.paragraphs output.run notenhanced

echo "============================================================="
echo "Running evaluation framework............."
echo "============================================================="

python ef_evaluate.py spritzer.cbor.hierarchical.qrels output.run

echo "============================================================="
echo "Generating results file with tagme enchanced queries........."
echo "============================================================="

python ef_ranking_document_generate.py spritzer.cbor.outlines spritzer.cbor.paragraphs output_tagme.run enhanced

echo "============================================================="
echo "Running evaluation framework on results on tagme enhanced results"
echo "============================================================="

python ef_evaluate.py spritzer.cbor.hierarchical.qrels output_tagme.run
