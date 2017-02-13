import re


class Qrel:
    def __init__(self, query_text, constant, _hash, relevance):
        self.query_text = query_text
        self.constant = constant
        self._hash = _hash
        self.relevance = relevance

    def get_query_text(self):
        return self.query_text

    def get_constant(self):
        return self.constant

    def get_hash(self):
        return self._hash

    def get_relevance(self):
        return self.relevance





