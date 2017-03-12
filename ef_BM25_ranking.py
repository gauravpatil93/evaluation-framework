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

    def average_length_of_documents(self):
        summ = 0.0
        for document in self.documents:
            summ += len(document[3])
        return summ / float(self.no_of_documents)


    def inverse_document_frequency(self, query_term):
        no_qi = self.no_of_documents_containing_qi(query_term)
        return float(math.log((self.no_of_documents - no_qi + 0.5) / (no_qi + 0.5)))

    def no_of_documents_containing_qi(self, query_word):
        count = 0
        for document in self.documents:
            for word in document[3]:
                if query_word == word:
                    count += 1
                    break
        return float(count)

    @staticmethod
    def term_frequency_in_a_document(query_term, document):
        count = 0
        for word in document.split():
            if query_term == word:
                count += 1
        return float(count)

    def const_value_calculation(self, document):
        return float(self.k * (1 - self.b + (self.b * len(document.split()) / self.average_length_of_documents)))

    def bm25_score(self, query, document_id, document):
        query_words = query[0].split()
        const_value = self.const_value_calculation(document)
        score = 0
        for query_term in query_words:
            term_freq = BM25.term_frequency_in_a_document(query_term, document)
            score += self.inverse_document_frequency(query_term) * \
                     ((term_freq * self.k_plus_one) / float(term_freq + const_value))
        tup = (query[1], document_id, score)
        return tup

    def get_no_of_documents(self):
        return self.no_of_documents

    def get_no_of_queries(self):
        return self.no_of_queries
