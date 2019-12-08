import pandas as pd
import operator


###################################################################
###########            Please Modify path          ################
###################################################################
path = "C:/Users/hahooon/Desktop/datamining_final/"



inverted_dic = pd.read_pickle(path + "sorted_inverted_file.pkl")
doc_list = pd.read_pickle(path + "doc_id.pkl")
all_doc = pd.read_pickle(path + "all_doc_txt.pkl")
josa_list = pd.read_pickle(path + "josa_list.pkl")
all_word_list = pd.read_pickle(path + "all_word_list.pkl")


def calc_weight(input_list):
    input_set = set(input_list)
    output_dic = {}
    for i in input_set:
        output_dic[i] = 0
    for w in input_set:
        output_dic[w] += round(input_list.count(w) / len(input_list), 3)
    return output_dic


def word_checker(q_list):
    output_list = []
    for w in q_list:
        if w in all_word_list:
            output_list.append(w)
    output_list += q_list
    output_list = list(set(output_list))
    return output_list


def check_stop_word(query):
    splt = query.split()
    output_list = []
    for q in splt:
        query_checker = True
        for j in josa_list:
            j_len = len(j)
            if j_len < len(q):
                if q[-1 * j_len:] == j:
                    output_list.append(q[:-1 * j_len])
                    query_checker = False
                    break
        if query_checker:
            output_list.append(q)
    return word_checker(output_list)


def print_r5(input_list, repeat):
    r5_list = derive_r5(input_list, repeat)
    print("-" * 90)
    for i in range(len(r5_list)):
        output_str = "|  Doc ID : \t" + str(r5_list[i][0]) + ",\t Document Name :" + str(r5_list[i][1])
        print(output_str)
    print("-" * 90)


def search_document(input_dic):
    input_list = list(input_dic.keys())
    temp_document = []
    doc_id_list = []
    output_list = []
    for k in input_list:
        if k in inverted_dic:
            temp_document.append(inverted_dic[k])

    for d in temp_document:
        temp_list = []
        for doc_tuple in d:
            temp_list.append(doc_tuple[0])

        doc_id_list.append(temp_list)

    equal_list = []
    length = len(doc_id_list)
    for first_idx in doc_id_list[0]:
        next_idx = 1
        in_checker = True
        while (next_idx != length):
            if first_idx not in doc_id_list[next_idx]:
                in_checker = False
                break
            next_idx += 1
        if in_checker:
            equal_list.append(first_idx)
    return equal_list


def search_more_than_one_arg(input_query):
    word_li = check_stop_word(query=input_query)
    weight = calc_weight(word_li)
    eq = search_document(weight)
    temp_output_dic = {}
    temp_dic = {}
    for k in list(weight.keys()):
        if k in inverted_dic:
            temp_dic[k] = inverted_dic[k]

    for k in temp_dic.keys():
        temp_li = []
        for t in temp_dic[k]:
            t1 = t[1]
            if t[0] in eq:
                t1 *= 2
            temp_li.append((t[0], t1 * weight[k]))
        temp_output_dic[k] = temp_li

    temp_result = []
    for k in temp_output_dic.keys():
        for t in temp_output_dic[k]:
            temp_result.append(t)

    result_output = sorted(temp_result, key=operator.itemgetter(1), reverse=True)
    return result_output


def search_one_arg(query):
    return inverted_dic[query]


def derive_r5(li, repeat):
    output_list = []
    for tupl in li[repeat:5 + repeat]:
        doc_id = tupl[0]
        output_list.append((doc_id, doc_list[doc_id]))
    return output_list


def run():
    print("Welcome Hahooni_i SE, if you want exit please Enter \'n'!!")
    while True:
        query = str(input("Please enter query : "))
        repeat = 0
        if query == 'n':
            print("Good Bye! - Hahoooni_i SE -")
            break

        query_list = check_stop_word(query)
        search_type = 0
        print_list = []
        print("System Query :\t" + str(query_list))
        if len(query_list) <= 1:
            if len(query_list) != 0:
                query = query_list[0]
            if query not in inverted_dic or len(inverted_dic[query]) == 0:
                print("Sorry, Our search Engine has not data about " + query + "!\nPlease another Search word...")
                continue
            print_list = search_one_arg(query)
        else:
            print_list = search_more_than_one_arg(query)
        print_r5(print_list, repeat)

        out_flag = False

        while True:
            print("If you want read Document, Please enter Doc ID,\t Else if you want exit, enter \'n'\n")
            print(
                "If you want to do more searches, Pleas enter \'c',  And you want more document about " + query + " Enter \'m'")
            doc_id = str(input("Enter\t:\t"))
            if doc_id == 'n':
                out_flag = True
                break
            if doc_id == 'c':
                break
            if doc_id == 'm':
                repeat += 5
                print_r5(print_list, repeat)
                continue
            if not (doc_id.isdigit()):
                print("You must enter Doc ID or [\'n', \'c', \'m']")
                continue
            print(all_doc[int(doc_id)])
        if out_flag:
            print("Good Bye! - Hahoooni_i SE -")
            break


if __name__ == "__main__":
    run()
