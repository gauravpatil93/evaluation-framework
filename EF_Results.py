import re


class Results:

    def __init__(self, query_text, Q0, document_id, rank, score, exp):
        self.query_text = query_text
        self.Q0 = Q0
        self.document_id = document_id
        self.rank = rank
        self.score = score
        self.exp = exp

    def get_query_text(self):
        return self.query_text

    def get_Q0(self):
        return self.Q0

    def get_document_id(self):
        return self.document_id

    def get_rank(self):
        return self.rank

    def get_score(self):
        return self.rank

    def get_exp(self):
        return self.exp

    def get_query_plan_text(self):
        query = self.query_text
        query = re.sub('%20', ' ', query)
        return query

