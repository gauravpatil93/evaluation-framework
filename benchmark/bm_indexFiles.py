#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Author Colin Etzel

INDEX_DIR = "benchmarkIndex.index."

import sys, os, lucene, threading, time
import argparse
from datetime import datetime

from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import \
    FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("inputFile", type=str, help="File of passages to index.")
args = vars(parser.parse_args())

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(Paths.get(storeDir))
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576, True) #no token limit
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, root, writer):

        t1 = FieldType()
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

        t2 = FieldType()
        t2.setStored(True)
        t2.setTokenized(True)
        t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        inFile = open(str(args["inputFile"]))
        indexName = inFile.readline()
        while(indexName != ''):
            print "adding", indexName
            doc = Document()
            doc.add(Field("name", indexName, t1))
            #doc.add(Field("path", root, t1))
            text = inFile.readline()
            if(len(text) > 0):
                print("contents: %s\n" %text)
                doc.add(Field("contents", text, t2))
            else:
                print "warning: no content in %s" %indexName
            indexName = inFile.readline()
            writer.addDocument(doc)
        inFile.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print IndexFiles.__doc__
        sys.exit(1)
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        IndexFiles(sys.argv[1], os.path.join(base_dir, INDEX_DIR),
                   StandardAnalyzer())
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e
