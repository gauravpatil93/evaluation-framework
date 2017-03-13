#!/bin/bash

python3 bm_passageExtractor.py spritzer.cbor.outlines spritzer.cbor.paragraphs paragraphs.txt
python3 bm_queryExtractor.py spritzer.cbor.outlines queries.txt
python bm_indexFiles.py paragraphs.txt
python bm_generateRankings.py queries.txt benchmark.run