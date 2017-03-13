#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Author Colin Etzel
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
parser.add_argument("outputFile", type=str, help="File of output in .run format")
args = vars(parser.parse_args())

class RankingEntry(object):
    """
    RankingEntry from trecCarTools, modified to work in python 2

    Attributes:
      paragraph    The content of the Paragraph (which in turn contain a list of ParaBodys)
      query_id: str  paragraph_id: str rank: int score: float exp_name=str=Node paragraph_content:str=None
    """
    def __init__(self, query_id, paragraph_id, rank, score, exp_name=None, paragraph_content=None):
        assert(rank > 0)
        self.query_id = query_id
        self.paragraph_id = paragraph_id
        self.rank = rank
        self.score = score
        self.exp_name = exp_name
        self.paragraph_content = paragraph_content

    def to_trec_eval_row(self, alternative_exp_name=None, page_only=False):
        exp_name_ = alternative_exp_name if alternative_exp_name is not  None \
                    else self.exp_name
        return [self.query_id, 'Q0', self.paragraph_id, self.rank, self.score, exp_name_]

"""
format_run also from trecCarTools
"""
def format_run(writer, ranking_of_paragraphs, exp_name=None):
    'write one ranking to the csv writer'
    for elem in ranking_of_paragraphs:
        writer.write(" ".join([str(x) for x in elem.to_trec_eval_row(exp_name)]))
        writer.write("\n")


def run(searcher, analyzer, queryList):
    runFile = open(args["outputFile"], "w")
    temp_list = []
    count = 0
    for tup in queryList:
        print "\nSearching for:", tup[0]
        formattedName = tup[1]
        query = QueryParser("contents", analyzer).parse(tup[0].replace("/","\/"))
        scoreDocs = searcher.search(query, 50).scoreDocs
        rank = 1
        print "%s total matching documents." % len(scoreDocs)
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            temp_list.append(RankingEntry(formattedName.replace("\n",""),str(doc.get("name")).replace("\n",""),rank,scoreDoc.score,'benchmark'))
            rank +=1
    format_run(runFile, temp_list, exp_name='benchmark')
    print("Wrote run file to %s" %args["outputFile"])
    runFile.close()




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