#!/bin/bash
echo "==========================================="
echo "Generating results file ................."
echo "==========================================="

python ef_ranking_document_generate.py spritzer.cbor.outlines spritzer.cbor.paragraphs output.run

echo "==========================================="
echo "Running evaluation framework............."
echo "==========================================="

python ef_evaluate.py spritzer.cbor.hierarchical.qrels output.run
