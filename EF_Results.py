import re


class Results:

    def __init__(self, query_text, Q0, _hash, rank, score, exp):
        self.query_text = query_text
        self.Q0 = Q0
        self._hash = _hash
        self.rank = rank
        self.score = score
        self.exp = exp
        self.num_queries = 0


    def get_query_text(self):
        return self.query_text

    def get_Q0(self):
        return self.Q0

    def get_hash(self):
        return self._hash

    def get_rank(self):
        return self.rank

    def get_score(self):
        return self.score

    def get_exp(self):
        return self.exp

    def get_query_plan_text(self):
        query = self.query_text
        query = re.sub('%20', ' ', query)
        return query

