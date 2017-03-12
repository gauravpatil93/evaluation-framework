import math


class BM25:
    def __init__(self, queries, documents):
        self.documents = documents
        self.queries = queries
        self.no_of_documents = len(documents)
        self.no_of_queries = len(queries)
        self.average_length_of_documents = self.average_length_of_documents()
        self.k = 1.2
        self.b = 0.75
        self.k_plus_one = self.k + 1
        self.BM25_value = []

    def average_length_of_documents(self):
        summ = 0
        for document in self.documents:
            summ += len(document.spilt())
        return summ / float(self.no_of_documents)

    def inverse_document_frequency(self, query_term):
        no_qi = self.no_of_documents_containing_qi(query_term)
        math.log((self.no_of_documents - no_qi + 0.5) / (no_qi + 0.5))

    def no_of_documents_containing_qi(self, query_word):
        count = 0
        for document in self.documents():
            for word in document[3].get_text().split():
                if query_word == word:
                    count += 1
                    break
        return count

    @staticmethod
    def term_frequency_in_a_document(query_term, document):
        count = 0
        for word in document.spilt():
            if query_term == word:
                count += 1
        return count

    def const_value_calculation(self, document):
        return self.k * (1 - self.b + self.b * len(document.split()) / self.average_length_of_documents)


        # def BM25_score(self, ):
