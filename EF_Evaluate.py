from EF_Qrel_parser import QrelParser
from EF_Results_parser import ResultsParser

qrel_obj = QrelParser("spritzer.cbor.hierarchical.qrels")
results_obj = ResultsParser("results")

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


match = 0
for queries in qrel_obj_list:
    for result in results_obj_list:
        if queries.get_query_text() == result.get_query_text() and queries.get_hash() == result.get_hash():
            match+=1

print(match)

