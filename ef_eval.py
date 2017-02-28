from ef_ir_results_parser import EfResultParser
from ef_qrery_parser import EfQueryParser


class Evaluate:
    def __init__(self, results_file_path, query_file_path):
        self.query_parser_object = EfQueryParser(query_file_path)
        self.result_parser_object = EfResultParser(results_file_path)
