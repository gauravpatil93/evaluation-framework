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

def format_run(writer, ranking_of_paragraphs, exp_name=None):
    'write one ranking to the csv writer'
    for elem in ranking_of_paragraphs:
        # query-number    Q0  document-id rank    score   Exp
        writer.write(" ".join([str(x) for x in elem.to_trec_eval_row(exp_name)]))
        writer.write("\n")

# Write the results to a file
"""
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
"""

def run(searcher, analyzer, queryList):
    runFile = open("benchmark.txt", "w")
    temp_list = []
    count = 0
    for tup in queryList:
        print "\nSearching for:", tup[0]
        formattedName = tup[1]
        #query = QueryParser("contents", analyzer).parse(tup[0].replace("/",""))
        query = QueryParser("contents", analyzer).parse(tup[0].replace("/","\/"))
        scoreDocs = searcher.search(query, 50).scoreDocs
        rank = 1
        #print "%s total matching documents." % len(scoreDocs)
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            temp_list.append(RankingEntry(formattedName.replace("\n",""),str(doc.get("name")).replace("\n",""),rank,scoreDoc.score,'benchmark'))
            #string = "%s Q0 %s %i %f benchmark\n" %(formattedName, str(doc.get("name")), rank, scoreDoc.score)
            rank +=1
            #string = string.replace("\n","")
            #runFile.write(string + "\n")
    format_run(runFile, temp_list, exp_name='benchmark')
    print("Gathered results")
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