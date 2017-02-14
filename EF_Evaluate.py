from EF_Qrel_parser import QrelParser
from EF_Results_parser import ResultsParser
import sys

# The Ground Truth file.
qrel_obj = QrelParser(sys.argv[1])
# The Result file from an IR.
results_obj = ResultsParser(sys.argv[2])

# The objects from the qrel file.
qrel_obj_list = qrel_obj.get_object_list()
# The objects from the IR result file.
results_obj_list = results_obj.get_object_list()

# This statement prints the RUN ID
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
    if qrel.get_relevance() is 1:
        rel_all += 1
print("num_rel_ret" + "\t all \t" + str(rel_all))

# Creating a list of query id's for future use
qrel_text_list = []
for qrel in qrel_obj_list:
    if qrel.get_relevance() is 1:
        qrel_text_list.append(qrel.get_query_text())
# This generates a list of query id that are unique
# Set eliminates duplicates
qrel_rem_dup = list(set(qrel_text_list))

# Creating a dict where query id's are keys and all the values
# are the list of objects entries matching that in the IR results file
# Although there no metric that directly depends on this dict
# This is useful for retrieving entries having a specific query id
# from the IR results file the lists obtained can then be sorted
# in an ascending order based on the rank.
result_of_each_query = dict()
for qrel_text in qrel_rem_dup:
    intermediate_list = []
    for result in results_obj_list:
        if qrel_text == result.get_query_text():
            intermediate_list.append(result)
    result_of_each_query[qrel_text] = list(intermediate_list)


def precision(qrel_object, _at=0):
    """
    This function calculates the precision at a specific rank
    :param qrel_object: This refers to objects of class EF_Qrel.
    :param _at: Rank
    :return: returns the precision at given rank
    """
    similar_list = []
    for objs in qrel_obj_list:
        if objs.get_relevance() is 1:
            if qrel_object.get_query_text() == objs.get_query_text():
                similar_list.append(objs.get_hash())
    temp_list = result_of_each_query[qrel_object.get_query_text()]
    # This function sorts the list of objects based on the rank (Ascending)
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


def average_precision(query_id):
    """
    This function calculates the average precision used by the mean average precsion
    calculation function
    :param query_id: query id string
    :return: average precision for a query
    """
    obj = []
    for m in qrel_obj_list:
        if m.get_relevance() is 1:
            if m.get_query_text() == query_id:
                obj.append(m)
    obj2 = []
    for n in results_obj_list:
        if n.get_query_text() == query_id:
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
    """
    This function calculates the mean_average_precision
    :return: map
    """
    sum = 0.0
    for result in result_text_dup:
        sum += average_precision(result)
    return sum / len(result_text_dup)


def average_precision_geo(query_id):
    """
    This function follows the same logic of the average precision
    function but returns 1.0 if there are no relevant query retrieved
    :param query_id:
    :return: average precision
    """
    obj = []
    for m in qrel_obj_list:
        if m.get_relevance() is 1:
            if m.get_query_text() == query_id:
                obj.append(m)
    obj2 = []
    for n in results_obj_list:
        if n.get_query_text() == query_id:
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
    """
    Calculates the geometric mean average precsion
    :return: gm_map
    """
    product = 1.0
    for result in result_text_dup:
        product *= average_precision_geo(result)
    return product ** (1/float(len(result_text_dup)))

# Prints map
print("map" + "\t all \t" + str(mean_average_precision()))

# Prints the gm_map
print("gm_map" + "\t all \t" + str(geometric_mean_average_precision()))


def r_precision(query_text):
    """
    This function calculates the R precision
    :param query_text: query string
    :return: Rpec
    """
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


def r_prec_average():
    """
    Calculates average Rpec
    :return: average Rpec
    """
    sum = 0.0
    for res in result_text_dup:
        sum += r_precision(res)
    return sum/len(result_text_dup)

print("Rpec" + "\t all \t" + str(r_prec_average()))


def reciprocal_rank(query_text):
    """
    Calculates the reciprocal rank
    :param query_text: query id
    :return: reciprocal_rank
    """
    obj = []
    for m in qrel_obj_list:
        if m.get_relevance() is 1:
            if m.get_query_text() == query_text:
                obj.append(m)
    obj2 = []
    for n in results_obj_list:
        if n.get_query_text() == query_text:
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
    """
    Returns the average reciprocal rank
    :return: recip_rank
    """
    sum = 0.0
    for res in result_text_dup:
        sum += reciprocal_rank(res)
    return sum/len(result_text_dup)

# Prints the average reciprocal rank
print("recip_rank" + "\t all \t" + str(reciprocal_rank_average()))


def precision_text(qrel_text, _at=0):
    """
    This method is similar to the precision method, the
    only difference is that instead of the object this method 
    takes the query string
    :param qrel_text: query string
    :param _at: rank
    :return:
    """
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
