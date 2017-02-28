class Query:
    def __init__(self, query_object_name):
        self.query_object_name = query_object_name
        self.query_list = []

    def add_query_to_object(self, tup):
        self.query_list.append(tup)

    def get_object_name(self):
        return self.query_object_name

    def get_query_list(self):
        return self.query_list

    def get_no_queries(self):
        return len(self.query_list)

    def calculate_no_of_relevant(self):
        no_of_relevant = 0
        for query in self.query_list:
            if query[3] == 1:
                no_of_relevant += 1
        return no_of_relevant

    def calculate_no_of_non_relevant(self):
        return self.get_no_queries() - self.calculate_no_of_relevant()
