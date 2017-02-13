from EF_Qrel_parser import QrelParser
from EF_Results_parser import ResultsParser
from pprint import pprint
import copy

qrel_obj = QrelParser("spritzer.cbor.hierarchical.qrels")
results_obj = ResultsParser("singlequery.results.txt")

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
                print(qrel.get_query_text() + "\t" + qrel.get_hash())
                match+=1

print("num_rel_ret" + "\t" + str(match))


def precision(_at):
    qrel_text_list = []
    for qrel in qrel_obj_list:
        if qrel.get_relevance() is 1:
            qrel_text_list.append(qrel.get_query_text())
    qrel_rem_dup = list(set(qrel_text_list))
    result_of_each_query = dict()

    for qrel_text in qrel_rem_dup:
        intermediate_list = []
        for result in results_obj_list:
            if qrel_text == result.get_query_text():
                intermediate_list.append(result)
        result_of_each_query.update({qrel_text : intermediate_list})
        intermediate_list.clear()
    pprint(result_of_each_query)






"""
qrel_text_list = []
for qrel in qrel_obj_list:
    if qrel.get_relevance() is 1:
        qrel_text_list.append(qrel.get_query_text())

result_text_list = []
for result in results_obj_list:
    result_text_list.append(result.get_query_text())

qrel_rem_dup = list(set(qrel_text_list))
result_text_dup = list(set(result_text_list))

pprint(set(qrel_rem_dup) - set(result_text_list))
"""





