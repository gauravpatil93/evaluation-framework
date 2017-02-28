from ef_ir_results_class import Result


class EfResultParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tup_list = []
        self.unique_result_list = self.generate_unique_result_list()
        self.result_objects_list = self.generate_result_object_list()

    def generate_unique_result_list(self):
        unique_result_list = []
        result_path = 0
        with open(self.file_path, 'r') as f:
            for line in f:
                line_list = line.split()
                self.tup_list.append((line_list[0], line_list[1], line_list[2], int(line_list[3]), float(line_list[4])
                                      , line_list[5]))
                result = line_list[result_path]
                unique_result_list.append(result)
        return list(set(unique_result_list))

    def generate_result_object_list(self):
        result_object_list = []
        result_location_in_tuple = 0
        for unique_result in self.unique_result_list:
            result_obj = Result(unique_result)
            for tup in self.tup_list:
                if unique_result == tup[result_location_in_tuple]:
                    # Give each object containing all the rows with the same query
                    # a name which in this case is the query_text
                    result_obj.add_result_to_object(tup)
            result_object_list.append(result_obj)
        return result_object_list

    def get_query_object_list(self):
        return self.result_objects_list

    def get_unique_query_list(self):
        return self.unique_result_list

    def get_all_row_from_file(self):
        return self.tup_list
