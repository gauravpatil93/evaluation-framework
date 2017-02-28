from ef_query_class import Query


class EfQueryParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tup_list = []
        self.unique_query_list = self.generate_unique_query_list()
        self.query_objects_list = self.generate_query_object_list()

    def generate_unique_query_list(self):
        unique_query_list = []
        query_path = 0
        with open(self.file_path, 'r') as f:
            for line in f:
                line_list = line.split()
                self.tup_list.append((line_list[0], int(line_list[1]), line_list[2], int(line_list[3])))
                query = line_list[query_path]
                unique_query_list.append(query)
        return list(set(unique_query_list))

    def generate_query_object_list(self):
        query_object_list = []
        query_location_in_tuple = 0
        for unique_query in self.unique_query_list:
            query_obj = Query(unique_query)
            for tup in self.tup_list:
                if unique_query == tup[query_location_in_tuple]:
                    # Give each object containing all the rows with the same query
                    # a name which in this case is the query_text
                    query_obj.add_query_to_object(tup)
            query_object_list.append(query_obj)
        return query_object_list

    def get_query_object_list(self):
        return self.query_objects_list

    def get_unique_query_list(self):
        return self.unique_query_list

    def get_all_row_from_file(self):
        return self.tup_list
