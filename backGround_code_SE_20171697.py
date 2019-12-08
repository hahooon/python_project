#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from tqdm import tqdm_notebook
import tqdm
import os
import operator
import math

'''
형태소 분석기를 돌린 후 해당 파일에 대해
명사를 추출해내면서 빈도수를 세는 함수 입니다.
'''
def make_freq(input_txt = ""):
    temp_str = input_txt
    tail = 0
    word_dic = {}
    pcnt = 0
    length = len(temp_str)
    while(tail < length-1):
        head, tail, flag= find_index(temp_str, tail)
        temp_pcnt = round(tail/length,3)*1000
        if(temp_pcnt == pcnt):
            print(str(temp_pcnt/10)+"% ...")
            pcnt += 1
        if flag: break
        word = temp_str[head+1:tail]
        if(checker(word)):
            if(word in word_dic.keys()):
                word_dic[word] += 1
            else:
                word_dic[word] = 1
    return word_dic


'''
make_freq 함수를 도와주기 위한 함수로
'\t'를 기준으로 단어에 대한 인덱스를 찾는
함수 입니다.
'''
def find_index(input_str = "", input_tail = 0):
    out_head = 0
    out_tail = len(input_str)-1
    flag, second_flag = False, True
    for ch, i in zip(input_str[input_tail:], range(len(input_str[input_tail:]))):
        if(ch == '\t'):
            out_head = input_tail + i
            flag = True
            break
    if(flag):
        for ch, i in zip(input_str[out_head+1:], range(1,len(input_str[out_head+1:]))):
            if(ch == '\n' or ch == '\t'):
                out_tail = out_head + i
                second_flag = False
                break
    return out_head, out_tail, second_flag


'''
해당 단어가 한국어 명사인지 확인하는 함수 입니다.
'''
def checker(string = ''):
    """ When appropriate input is entered, the function returns
    boolean True. (input must be in Korean Unicode range) """
    for c in string:
        ord_num = ord(c)
        if 44023 > ord_num or ord_num > 55203:
            return False
    return True


# In[2]:


#f_list = os.listdir("C:/Users/hahooon/Desktop/datamining_final/ITnews623_sim383/")

#pd.to_pickle(f_list, path="C:/Users/hahooon/Desktop/datamining_final/doc_id.pkl")


# In[2]:


doc_list = pd.read_pickle("C:/Users/hahooon/Desktop/datamining_final/doc_id.pkl")
word_dic = pd.read_pickle("C:/Users/hahooon/Desktop/datamining_final/word_dic.pkl")
sorted_word_dic = pd.read_pickle("C:/Users/hahooon/Desktop/datamining_final/tf_dic.pkl")
backword_id_dic = pd.read_pickle("C:/Users/hahooon/Desktop/datamining_final/backword_id.pkl")
word_ic_dic = pd.read_pickle("C:/Users/hahooon/Desktop/datamining_final/forward_ip.pkl")
inverted_dic = pd.read_pickle("C:/Users/hahooon/Desktop/datamining_final/inverted_file.pkl")


# In[4]:


#f = open('C:/Users/hahooon/Desktop/datamining_final/final_out.txt', encoding='ansi')
#doc_str = f.readlines()

#all_str = ""
#for con in tqdm_notebook(doc_str):
#    all_str+=con


# In[31]:


#word_dic = make_freq(all_str)

#pd.to_pickle(word_dic, path="C:/Users/hahooon/Desktop/datamining_final/word_dic.pkl")


# In[8]:





# In[12]:


temp_word_dic = sorted(word_dic.items(), key=operator.itemgetter(1), reverse=True)


# In[13]:


"""
sorted_word_dic = {}
word_id_dic = {}
backword_id_dic = {}
for t, i in tqdm_notebook(zip(temp_word_dic, range(len(temp_word_dic)))):
    sorted_word_dic[t[0]] = t[1]
    word_id_dic[t[0]] = i
    backword_id_dic[i] = t[0]

pd.to_pickle(sorted_word_dic, path="C:/Users/hahooon/Desktop/datamining_final/tf_dic.pkl")
pd.to_pickle(backword_id_dic, path="C:/Users/hahooon/Desktop/datamining_final/backword_id.pkl")
pd.to_pickle(word_id_dic, path="C:/Users/hahooon/Desktop/datamining_final/forward_ip.pkl")"""

##################################################################################################
##################################################################################################
############################### 중간 보고서 까지 진행 상황 ##########################################
##################################################################################################
##################################################################################################


# In[15]:


"""
-all_doc 에 ITnews623_sim383에 있는 문서들의 내용을 모두 담는다.
         all_doc 은 밑에서 tf, df를 구하는데 사용된다.
-metric 은 metric[doc_id][word_id]로 접근이 가능하다.
         metric에는 tf-idf를 계산한 값이 저장된다.
"""

all_doc = []
for newsName in tqdm_notebook(doc_list):
    temp_file = open("C:/Users/hahooon/Desktop/datamining_final/ITnews623_sim383/" + newsName, "r", encoding='ansi')
    all_doc.append(temp_file.read())
    temp_file.close()

metric = []
for _ in range(len(doc_list)):
    metric.append({})
    
for word_id in tqdm_notebook(range(len(word_id_dic))):
    word = backword_id_dic[word_id]
    for doc, doc_id in zip(all_doc, range(len(all_doc))):
        if word in doc:
            metric[doc_id][word_id] = all_doc[doc_id].count(word)
        else:
            metric[doc_id][word_id] = 0
            
pd.to_pickle(metric, path="C:/Users/hahooon/Desktop/datamining_final/metric_with_tf.pkl")


# In[18]:


idf = []
for word_id in tqdm_notebook(range(len(metric[0]))):
    doc_cnt = 0
    for doc_id in range(len(metric)):
        if metric[doc_id][word_id] > 0:
            doc_cnt += 1
    idf.append(math.log(len(metric)/(doc_cnt+1)))


# In[19]:


for word_id in tqdm_notebook(range(len(metric[0]))):
    for doc_id in range(len(metric)):
        metric[doc_id][word_id] *= idf[word_id]


# In[27]:


pd.to_pickle(metric, path="C:/Users/hahooon/Desktop/datamining_final/metric_with_tf_idf.pkl")


# In[28]:


pd.to_pickle(idf, path="C:/Users/hahooon/Desktop/datamining_final/idf_list.pkl")


# In[47]:


backward_index_table = []

for doc_id in tqdm_notebook(range(len(metric))):
    temp_list = sorted(metric[doc_id].items(), key=operator.itemgetter(1), reverse=True)
    backward_index_table.append(temp_list)


# In[55]:


pd.to_pickle(backward_index_table, path="C:/Users/hahooon/Desktop/datamining_final/backward_index_table.pkl")


# In[64]:


inverted_dic = {}
for word_id in tqdm_notebook(range(len(backword_id_dic))):
    doc_id_tf_idf_list = []
    for doc_id in range(len(metric)):
        if metric[doc_id][word_id] > 0:
            doc_id_tf_idf_list.append((doc_id, metric[doc_id][word_id]))
    inverted_dic[backword_id_dic[word_id]] = doc_id_tf_idf_list


# In[81]:


pd.to_pickle(inverted_dic, path="C:/Users/hahooon/Desktop/datamining_final/inverted_file.pkl")


# In[107]:


inverted_dic = pd.read_pickle("C:/Users/hahooon/Desktop/datamining_final/inverted_file.pkl")


# In[108]:


for word_id in tqdm_notebook(range(len(inverted_dic))):
    term = backword_id_dic[word_id]
    inverted_dic[term] = sorted(inverted_dic[term], key=operator.itemgetter(1), reverse=True)


# In[111]:


pd.to_pickle(inverted_dic, path="C:/Users/hahooon/Desktop/datamining_final/sorted_inverted_file.pkl")


# In[ ]:


posting_file = []
term_table = {}


# In[159]:


def search_one_arg():
    query = str(input("Please enter one word : "))
    r5_list = derive_r5(inverted_dic[query])
    length = len("--------------------------------------------------------------------------------------")
    print("--------------------------------------------------------------------------------------")
    for i in range(len(r5_list)):
        output_str = "|  Doc ID : \t" + str(r5_list[i][0]) + ",\t Document Name :" + str(r5_list[i][1])
        print(output_str)
    print("--------------------------------------------------------------------------------------")


# In[121]:


def derive_r5(li):
    output_list = []
    for tupl in li[:5]:
        doc_id = tupl[0]
        output_list.append((doc_id, doc_list[doc_id]))
    return output_list


# In[168]:


pd.to_pickle(all_doc, path="C:/Users/hahooon/Desktop/datamining_final/all_doc_txt.pkl")


# In[ ]:





# In[186]:


word_all_str=[]
f_list = os.listdir("C:/Users/hahooon/Desktop/datamining_final/word_list/")
for f_name in f_list:
    f = open("C:/Users/hahooon/Desktop/datamining_final/word_list/"+f_name)
    temp_str = f.read()
    for j in tqdm_notebook(temp_str.split('\n')):
        word_all_str.append(j)


# In[201]:


pd.to_pickle(word_all_str, path="C:/Users/hahooon/Desktop/datamining_final/all_word_list.pkl")


# In[179]:


f = open("C:/Users/hahooon/Desktop/datamining_final/word_list/1.txt")


# In[180]:


f_str = f.read()


# In[183]:


f_str.split('\n')


# In[ ]:





# In[206]:


f = open("C:/Users/hahooon/Desktop/datamining_final/josa_top90.txt", encoding='ansi')


# In[207]:


f_str = f.read()


# In[210]:


f_splt = f_str.split()


# In[211]:


f_set = set(f_splt)


# In[214]:


pd.to_pickle(f_set, path="C:/Users/hahooon/Desktop/datamining_final/josa_set.pkl")


# In[ ]:




