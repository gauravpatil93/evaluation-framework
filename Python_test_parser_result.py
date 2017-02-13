from Python_test_results import Results


class ResultsParser:

    def __init__(self, file_path):
        self.file_path = file_path

    def get_object_list(self):
        object_list = list()
        with open(self.file_path, 'r') as f:
            for line in f:
                line_list = line.split()
                results_object = Results(int(line_list[0]), line_list[1], line_list[2], int(line_list[3]),
                                      float(line_list[4]), line_list[5])
                object_list.append(results_object)
        return object_list





