from Python_test_parser import QrelParser
from Python_test_parser_result import ResultsParser

qrel_obj = QrelParser("qrels.test")
results_obj = ResultsParser("results.test")

qrel_obj_list = qrel_obj.get_object_list()
results_obj_list = results_obj.get_object_list()

# Run ID
print("run_id" + "\t" + results_obj_list[0].get_exp())

# Total number of documents retrieved over all queries
print("num_ret" + "\t" + str(len(results_obj_list)))

# Total number of relevant documents over all queries
rel_all = 0
for qrel in qrel_obj_list:
    if qrel.get_relevance() == 1:
        rel_all += 1
print("num_rel" + "\t" + str(rel_all))

# Total number of relevant documents retrieved over all queries
match = 0
for qrel in qrel_obj_list:
    if qrel.get_relevance() is 1:
        for result in results_obj_list:
            if (qrel.get_query_text() == result.get_query_text()) and (qrel.get_hash() == result.get_hash()):
                match+=1

print("num_rel_ret" + "\t" + str(match))

