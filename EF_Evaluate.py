from EF_Qrel_parser import QrelParser
from EF_Results_parser import ResultsParser
import sys

qrel_obj = QrelParser(sys.argv[1])
results_obj = ResultsParser(sys.argv[2])

qrel_obj_list = qrel_obj.get_object_list()
results_obj_list = results_obj.get_object_list()

# Run ID
print("runid" + "\t all \t" + results_obj_list[0].get_exp())

result_text_list = []
for result in results_obj_list:
    result_text_list.append(result.get_query_text())
result_text_dup = list(set(result_text_list))
print("num_q" + "\t all \t" + str(len(result_text_dup)))


# Total number of documents retrieved over all queries
print("num_ret" + "\t all \t" + str(len(results_obj_list)))

# Total number of relevant documents over all queries
rel_all = 0
for qrel in qrel_obj_list:
    if qrel.get_relevance() == 1:
        rel_all += 1
print("num_rel_ret" + "\t all \t" + str(rel_all))

# Total number of relevant documents retrieved over all queries
match = 0
for qrel in qrel_obj_list:
    if qrel.get_relevance() is 1:
        for result in results_obj_list:
            if (qrel.get_query_text() == result.get_query_text()) and (qrel.get_hash() == result.get_hash()):
                #print(qrel.get_query_text() + "\t" + qrel.get_hash())
                match+=1


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
    result_of_each_query[qrel_text] = list(intermediate_list)


def precision(qrel_object, _at=0):
    similar_list = []
    for objs in qrel_obj_list:
        if objs.get_relevance() is 1:
            if qrel_object.get_query_text() == objs.get_query_text():
                similar_list.append(objs.get_hash())
    temp_list = result_of_each_query[qrel_object.get_query_text()]
    temp_list.sort(key=lambda x: x.get_rank())
    no_of_occurences = 0.0
    if _at == 0:
        _at = len(temp_list)
    if _at > len(temp_list):
        for x in temp_list:
            if x.get_hash() in similar_list:
                no_of_occurences += 1
    else:
        for x in temp_list[:_at]:
            if x.get_hash() in similar_list:
                no_of_occurences += 1
    return no_of_occurences/_at


def average_precision(qrel_text):
    obj = []
    for m in qrel_obj_list:
        if m.get_query_text() == qrel_text:
            obj.append(m)
    obj2 = []
    for n in results_obj_list:
        if n.get_query_text() == qrel_text:
            obj2.append(n)
    obj3 = []
    for x in obj:
        for y in obj2:
            if (x.get_query_text() == y.get_query_text()) and (x.get_hash() == y.get_hash()):
                obj3.append(y)
    sum = 0.0
    for objs in obj3:
        sum += precision(objs, objs.get_rank())
    if len(obj3) == 0:
        return 0.0
    else:
        return sum / len(obj3)


def mean_average_precision():
    sum = 0.0
    for result in result_text_dup:
        sum += average_precision(result)
    return sum / len(result_text_dup)

print("map" + "\t all \t" + str(mean_average_precision()))

def average_precision_geo(qrel_text):
    obj = []
    for m in qrel_obj_list:
        if m.get_query_text() == qrel_text:
            obj.append(m)
    obj2 = []
    for n in results_obj_list:
        if n.get_query_text() == qrel_text:
            obj2.append(n)
    obj3 = []
    for x in obj:
        for y in obj2:
            if (x.get_query_text() == y.get_query_text()) and (x.get_hash() == y.get_hash()):
                obj3.append(y)
    sum = 0.0
    for objs in obj3:
        sum += precision(objs, objs.get_rank())
    if len(obj3) == 0:
        return 1.0
    else:
        return sum / len(obj3)


def geometric_mean_average_precision():
    product = 1.0
    for result in result_text_dup:
        product *= average_precision_geo(result)
    return product ** (1/float(len(result_text_dup)))

print("gm_map" + "\t all \t" + str(geometric_mean_average_precision()))


def r_precision(query_text):
    similar_list = []
    for objs in qrel_obj_list:
        if objs.get_relevance() is 1:
            if query_text == objs.get_query_text():
                similar_list.append(objs.get_hash())
    r = len(similar_list)
    temp_list = result_of_each_query[query_text]
    temp_list.sort(key=lambda x: x.get_rank())
    no_of_occurences = 0.0
    if r == 0:
        r = len(temp_list)
    if r > len(temp_list):
        for x in temp_list:
            if x.get_hash() in similar_list:
                no_of_occurences += 1
    else:
        for x in temp_list[:r]:
            if x.get_hash() in similar_list:
                no_of_occurences += 1
    return no_of_occurences/r


def r_prec_call():
    sum = 0.0
    for res in result_text_dup:
        sum += r_precision(res)
    return sum/len(result_text_dup)

print("Rpec" + "\t all \t" + str(r_prec_call()))


def reciprocal_rank(qrel_text):
    obj = []
    for m in qrel_obj_list:
        if m.get_relevance() is 1:
            if m.get_query_text() == qrel_text:
                obj.append(m)
    obj2 = []
    for n in results_obj_list:
        if n.get_query_text() == qrel_text:
            obj2.append(n)
    obj2.sort(key=lambda x: x.get_rank())
    val = 0.0
    for x in obj:
        for y in obj2:
            if (x.get_query_text() == y.get_query_text()) and (x.get_hash() == y.get_hash()):
                val = 1/float(y.get_rank())
                break
        break
    return val


def reciprocal_rank_average():
    sum = 0.0
    for res in result_text_dup:
        sum += reciprocal_rank(res)
    return sum/len(result_text_dup)

print("recip_rank" + "\t all \t" + str(reciprocal_rank_average()))

def precision_text(qrel_text, _at=0):
    similar_list = []
    for objs in qrel_obj_list:
        if objs.get_relevance() is 1:
            if qrel_text == objs.get_query_text():
                similar_list.append(objs.get_hash())
    temp_list = result_of_each_query[qrel_text]
    temp_list.sort(key=lambda x: x.get_rank())
    no_of_occurences = 0.0
    if _at == 0:
        _at = len(temp_list)
    if _at > len(temp_list):
        for x in temp_list:
            if x.get_hash() in similar_list:
                no_of_occurences += 1
    else:
        for x in temp_list[:_at]:
            if x.get_hash() in similar_list:
                no_of_occurences += 1
    return no_of_occurences/_at


def precision_text_average():
    sum = 0.0
    for elem in result_text_dup:
        sum += precision_text(elem, 5)
    print("P_5" + "\t all \t" + str(sum/len(result_text_dup)))
    sum = 0.0
    for elem in result_text_dup:
        sum += precision_text(elem, 10)
    print("P_10" + "\t all \t" + str(sum / len(result_text_dup)))
    sum = 0.0
    for elem in result_text_dup:
        sum += precision_text(elem, 15)
    print("P_15" + "\t all \t" + str(sum / len(result_text_dup)))
    sum = 0.0
    for elem in result_text_dup:
        sum += precision_text(elem, 20)
    print("P_20" + "\t all \t" + str(sum / len(result_text_dup)))
    sum = 0.0
    for elem in result_text_dup:
        sum += precision_text(elem, 30)
    print("P_30" + "\t all \t" + str(sum / len(result_text_dup)))
    sum = 0.0
    for elem in result_text_dup:
        sum += precision_text(elem, 100)
    print("P_100" + "\t all \t" + str(sum / len(result_text_dup)))
    sum = 0.0
    for elem in result_text_dup:
        sum += precision_text(elem, 200)
    print("P_200" + "\t all \t" + str(sum / len(result_text_dup)))
    sum = 0.0
    for elem in result_text_dup:
        sum += precision_text(elem, 500)
    print("P_500" + "\t all \t" + str(sum / len(result_text_dup)))
    sum = 0.0
    for elem in result_text_dup:
        sum += precision_text(elem, 1000)
    print("P_1000" + "\t all \t" + str(sum / len(result_text_dup)))

precision_text_average()

def recall(query_text):
    similar_list = []
    for objs in qrel_obj_list:
        if objs.get_relevance() is 1:
            if query_text == objs.get_query_text():
                similar_list.append(objs)
    no_of_relevent = len(similar_list)
    no_of_rel_and_ret = 0.0
    temp_list = result_of_each_query[query_text]
    for elem in temp_list:
        for elem2 in similar_list:
            if (elem.get_query_text() ==  elem2.get_query_text()) and (elem2.get_hash() == elem.get_hash()):
                no_of_rel_and_ret+=1
    return no_of_rel_and_ret/no_of_relevent

