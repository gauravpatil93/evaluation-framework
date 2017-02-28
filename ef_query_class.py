class Query:
    def __init__(self, query_object_name):
        """
        Constructor takes the query_object_name as a parameter
        Every query object is identified by the query text i.e. the
        % separated string
        For example a query object with name 'Sustainable%20biofuel/Biofuel%20options'
        has the the following rows from the query files as tuples

        Sustainable%20biofuel/Biofuel%20options 0 1a61601e89d7a7bee5261b2375fa3a1958e473a2 1
        Sustainable%20biofuel/Biofuel%20options 0 465c78c1ed370aab4b3d3557c7ae002e6d7965ee 1
        Sustainable%20biofuel/Biofuel%20options 0 94a1c1dcf64c06fba3e8c1277f5ad7c0f0b8aea6 1
        Sustainable%20biofuel/Biofuel%20options 0 fd318050bd819ac1ef4d0815eb2291a5c874d552 1

        :param query_object_name: String
        """
        self.query_object_name = query_object_name
        self.query_list = []

    def add_query_to_object(self, tup):
        """
        This method adds a query from the text file in the form a tuple to the queries
        having the same query text
        :param tup: tuple

        The tuple can be
        (Sustainable%20biofuel/Biofuel%20options, 0, 1a61601e89d7a7bee5261b2375fa3a1958e473a2, 1)
        """
        self.query_list.append(tup)

    def get_object_name(self):
        """
        This just returns the object name
        :return: String

        Example: Sustainable%20biofuel/Biofuel%20options
        """
        return self.query_object_name

    def get_query_list(self):
        """
        This returns the query list i.e. list of all rows in a file
        have the same query text
        :return: List()
        """
        return self.query_list

    def get_no_queries(self):
        """
        Returns the no of rows with the same query text
        :return: int
        """
        return len(self.query_list)

    def calculate_no_of_relevant(self):
        """
        Returns the no of relevant queries
        :return: int
        """
        no_of_relevant = 0
        for query in self.query_list:
            if query[3] == 1:
                no_of_relevant += 1
        return no_of_relevant

    def calculate_no_of_non_relevant(self):
        """
        Returns the no of non-relevant queries
        :return: int
        """
        return self.get_no_queries() - self.calculate_no_of_relevant()
