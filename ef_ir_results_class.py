class Result:
    def __init__(self, result_object_name):
        """
        The constructor constructs the object in a similar way to how
        the Query class constructs all the rows with the same query text are put
        into one result object and the the query text is the name of this object

        For Example: Spent%20nuclear%20fuel/Risks

        The list in this class would contain the following queries from the file

        Spent%20nuclear%20fuel/Risks Q0 24e6153adbca79a47eaae274d5d7498537f4fcbf 1 1.0 mock
        Spent%20nuclear%20fuel/Risks Q0 e44dbe69bce8497314edae9add6f303ace0a62b9 2 0.5 mock
        Spent%20nuclear%20fuel/Risks Q0 2a2312ec3c829353aa36b943a19b2cf7df1ce944 3 0.3333333333333333 mock
        Spent%20nuclear%20fuel/Risks Q0 c800eba89bb803851b57e5138a47fe4f5ca34557 4 0.25 mock
        Spent%20nuclear%20fuel/Risks Q0 d6db1e404f669f4a0da820b42be9465736aabd3e 5 0.2 mock
        Spent%20nuclear%20fuel/Risks Q0 8c7f6a631363114f95233721ed05319f56d247d7 6 0.16666666666666666 mock
        Spent%20nuclear%20fuel/Risks Q0 af3d96aef1f62846d88a77fe8fdf35b1bb7a8753 7 0.14285714285714285 mock
        Spent%20nuclear%20fuel/Risks Q0 bd4e0086493a556490a9d4bb75f9f575071a09a5 8 0.125 mock
        Spent%20nuclear%20fuel/Risks Q0 850514874dabae44da05115c88836e852f11715e 9 0.1111111111111111 mock
        Spent%20nuclear%20fuel/Risks Q0 052666868089ae2aa4ec547595f2178792cb916b 10 0.1 mock
        :param result_object_name:
        """
        self.result_object_name = result_object_name
        self.result_list = []

    def add_result_to_object(self, tup):
        """
        This function adds the tuples aka rows having the same query text into the list
        that is a part of this object
        :param tup: tuple()

        For example this is a valid tuple that can be added into the object if the object name is
        Spent%20nuclear%20fuel/Risks

        (Spent%20nuclear%20fuel/Risks, Q0, 24e6153adbca79a47eaae274d5d7498537f4fcbf, 1, 1.0, mock)
        """
        self.result_list.append(tup)

    def get_object_name(self):
        """
        Returns the object name
        :return: str()
        """
        return self.result_object_name

    def get_result_list(self):
        """
        Gets the list of tuples corresponding to the object name i.e.
        returns the list having all rows in the form of tuples with the
        same query text
        :return: list()
        """
        return self.result_list
