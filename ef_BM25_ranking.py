import math


class BM25:
    def __init__(self, queries: list, documents: list):
        """
        Pass the query and document lists
        :param queries: The query is a list of tuples of (p1, p2, p3)

        p1 : The space separated query.
        p2 : The % separated query.
        p3 : An list consisting of the individual query terms

        :param documents: The document list is a list of tuples (p1, p2, p3, p4)

         p1: The document ID
         p2: No of words in the document
         p3: The text in the document
         p4: List of words in the document

         For more information scroll down to BM25 calculation to see the formatting of the aforementioned
         params
        """
        self.documents = documents
        self.queries = queries
        self.no_of_documents = float(len(documents))
        self.no_of_queries = len(queries)
        self.average_length_of_documents = self.average_length_of_documents()
        self.k = 1.2
        self.b = 0.75
        self.k_plus_one = self.k + 1

    def average_length_of_documents(self):
        """
        Calculates the average length of documents
        :return: Avg length of documents
        """
        summ = 0.0
        for document in self.documents:
            summ += document[1]
        return summ / float(self.no_of_documents)

    def inverse_document_frequency(self, query_term):
        """
        Inverse document frequency with smoothing factor
        :param query_term: A word from the query
        :return: IDF
        """
        no_qi = self.no_of_documents_containing_qi(query_term)
        return float(math.log(self.no_of_documents / (no_qi + 1.0)))

    def no_of_documents_containing_qi(self, query_word):
        """
        No of documents containing the word from the query
        :param query_word: A word from the query
        :return: No of documents that contain the word
        """
        count = 0
        for document in self.documents:
            for word in document[3]:
                if query_word == word:
                    count += 1
                    break
        return float(count)

    @staticmethod
    def term_frequency_in_a_document(query_term, document_words_list):
        """
        This calculates the occurrence of a word in a document
        :param query_term: A word from the query
        :param document_words_list: List of words in the document
        :return: No of times a word occurs in a document
        """
        count = 0
        for word in document_words_list:
            if query_term == word:
                count += 1
        return float(count)

    def const_value_calculation(self, document_length):
        """
        This method optimized the calculation of the k * (1 - b + b * |D| / avgdl )
        :param document_length: document length
        :return: k * (1 - b + b * |D| / avgdl )
        """
        return float(self.k * (1 - self.b + (self.b * document_length / self.average_length_of_documents)))

    def bm25_score(self, query, document):
        """
        This method returns the score for a specific query on a specific document.
        :param query: ('Spent nuclear fuel Nature of spent fuel Nanomaterial properties',
        'Spent%20nuclear%20fuel/Nature%20of%20spent%20fuel/Nanomaterial%20properties',
        ['Spent', 'nuclear', 'fuel', 'Nature', 'of', 'spent', 'fuel', 'Nanomaterial', 'properties'])

        The query is a list of tuples of (p1, p2, p3)

        p1 : The space separated query.
        p2 : The % separated query.
        p3 : An list consisting of the individual query terms.

        :param document: ('00e44bea6094085d44b2493d4d48a66358518d35', 198, 'cayman turtle farm located in grand cayman
        in the northwest caribbean sea is the first farm to have achieved the second generation of green sea turtles
        bred laid hatched and raised in captivity  since its beginning in 1968 the farm has released over 31000 turtles
         into the wild and each year more captive-bred turtles are released into the caribbean sea from beaches around
         the island of grand cayman captive-bred turtles released from the farm as hatchlings or yearlings with "living
         tags" have now begun to return to nest on grand cayman as adults   on february 19 2012 the farm released the
         first 2nd-generation captive-bred green sea turtle equipped with a position tracking transponder – ptt
         (also known as a satellite tag)   in addition the farm provides turtle meat products to the local population
         for whom turtle has been part of the traditional cuisine for centuries in so doing the farm curtails the
         incentive to take turtles from the wild which over the years in addition to the cayman turtle farm\'s release
         of captive-bred turtles has enabled an increase in the number of turtles sighted in the waters around the
         island of grand cayman and nesting on its beaches', ['cayman', 'turtle', 'farm', 'located', 'in', 'grand',
         'cayman', 'in', 'the', 'northwest', 'caribbean', 'sea', 'is', 'the', 'first', 'farm', 'to', 'have', 'achieved'
         , 'the', 'second', 'generation', 'of', 'green', 'sea', 'turtles', 'bred', 'laid', 'hatched', 'and', 'raised',
         'in', 'captivity', 'since', 'its', 'beginning', 'in', '1968', 'the', 'farm', 'has', 'released', 'over', '31000'
         , 'turtles', 'into', 'the', 'wild', 'and', 'each', 'year', 'more', 'captive-bred', 'turtles', 'are', 'released'
         , 'into', 'the', 'caribbean', 'sea', 'from', 'beaches', 'around', 'the', 'island', 'of', 'grand', 'cayman',
         'captive-bred', 'turtles', 'released', 'from', 'the', 'farm', 'as', 'hatchlings', 'or', 'yearlings', 'with',
         '"living', 'tags"', 'have', 'now', 'begun', 'to', 'return', 'to', 'nest', 'on', 'grand', 'cayman', 'as',
         'adults', 'on', 'february', '19', '2012', 'the', 'farm', 'released', 'the', 'first', '2nd-generation',
         'captive-bred', 'green', 'sea', 'turtle', 'equipped', 'with', 'a', 'position', 'tracking', 'transponder',
         '–', 'ptt', '(also', 'known', 'as', 'a', 'satellite', 'tag)', 'in', 'addition', 'the', 'farm', 'provides',
         'turtle', 'meat', 'products', 'to', 'the', 'local', 'population', 'for', 'whom', 'turtle', 'has', 'been',
         'part', 'of', 'the', 'traditional', 'cuisine', 'for', 'centuries', 'in', 'so', 'doing', 'the', 'farm',
         'curtails', 'the', 'incentive', 'to', 'take', 'turtles', 'from', 'the', 'wild', 'which', 'over', 'the',
         'years', 'in', 'addition', 'to', 'the', 'cayman', 'turtle', "farm's", 'release', 'of', 'captive-bred',
         'turtles', 'has', 'enabled', 'an', 'increase', 'in', 'the', 'number', 'of', 'turtles', 'sighted', 'in',
         'the', 'waters', 'around', 'the', 'island', 'of', 'grand', 'cayman', 'and', 'nesting', 'on', 'its', 'beaches'])

         The document list is a list of tuples (p1, p2, p3, p4)

         p1: The document ID
         p2: No of words in the document
         p3: The text in the document
         p4: List of words in the document

        :return: tuple (p1, p2, p3)

        p1: % separated query
        p2: document ID
        p3: score

        """
        query_words = query[2]
        const_value = self.const_value_calculation(document[1])
        score = 0
        for query_term in query_words:
            term_freq = BM25.term_frequency_in_a_document(query_term, document[3])
            score += self.inverse_document_frequency(query_term) * (
            (term_freq * self.k_plus_one) / float(term_freq + const_value))
        tup = (query[1], document[0], score)
        return tup

    def get_no_of_documents(self):
        """
        Returns the no of documents
        :return: int
        """
        return self.no_of_documents

    def get_no_of_queries(self):
        """
        Returns the no of queries
        :return: int
        """
        return self.no_of_queries

    def get_average_length_of_documents(self):
        """
        Returns the average length of the documents
        :return: int
        """
        return self.average_length_of_documents
