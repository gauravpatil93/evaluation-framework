from EF_Qrel import Qrel


class Qrel_parser:

    def __init__(self, file_path):
        self.file_path = file_path

    def get_object_list(self):
        object_list = list()
        with open(self.file_path, 'r') as f:
            for line in f:
                line_list = line.split()
                qrel_obj = Qrel(line_list[0], int(line_list[1]), line_list[2], int(line_list[3]))
                object_list.append(qrel_obj)
        return object_list





