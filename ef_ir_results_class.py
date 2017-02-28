class Result:
    def __init__(self, result_object_name):
        self.result_object_name = result_object_name
        self.result_list = []

    def add_result_to_object(self, tup):
        self.result_list.append(tup)

    def get_object_name(self):
        return self.result_object_name

    def get_result_list(self):
        return self.result_list
