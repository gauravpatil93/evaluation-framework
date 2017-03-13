#!/usr/bin/env python
#-*- coding: utf-8 -*-
INDEX_DIR = "benchmarkIndex.index."

import sys, os, lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search.similarities import ClassicSimilarity

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("queryFile", type=str, help="File of queries to run.")
args = vars(parser.parse_args())

def run(searcher, analyzer, queryList):
    runFile = open("benchmark.run", "w")
    for tup in queryList:
        print "\nSearching for:", tup[0]
        formattedName = tup[1]
        query = QueryParser("contents", analyzer).parse(tup[0].replace("/",""))
        scoreDocs = searcher.search(query, 50).scoreDocs
        rank = 1
        print "%s total matching documents." % len(scoreDocs)
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            string = "%s Q0 %s %i %f benchmark\n" %(formattedName, str(doc.get("name")), rank, scoreDoc.score)
            rank +=1
            string = string.replace("\n","")
            runFile.write(string + "\n")


def makeQueryList(fileName):
    queryList = []
    queryFile = open(fileName)
    plainQuery = queryFile.readline()
    while(plainQuery != ''):
        formatQuery = queryFile.readline()
        queryList.append((plainQuery, formatQuery))
        plainQuery = queryFile.readline()
    queryFile.close()
    return queryList


def main():
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    
    queries = makeQueryList(args["queryFile"])
    print 'lucene', lucene.VERSION
    print "\n"

    directory = SimpleFSDirectory(Paths.get(os.getcwd(), INDEX_DIR))
    print directory.getDirectory()
    searcher = IndexSearcher(DirectoryReader.open(directory))
    searcher.setSimilarity(ClassicSimilarity())
    analyzer = StandardAnalyzer()
  
    run(searcher, analyzer, queries)
    del searcher

main()