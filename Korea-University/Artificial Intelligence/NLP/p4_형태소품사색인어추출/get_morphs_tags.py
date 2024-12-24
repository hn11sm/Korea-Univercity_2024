#!/usr/bin/env python3
# coding: utf-8

import sys

###############################################################################
# 형태소 분석 결과로부터 형태소와 품사들을 알아냄 +/SW++/SW
# return value : (형태소, 품사)로 구성된 tuple들의 list
def get_morphs_tags(tagged):
    result = []
    list_tagged = list(tagged)
    if list_tagged[0]== '+':
        list_tagged[0] = '__PLuS__'

    for i in range(1, len(list_tagged)):
        if list_tagged[i-1] == '+' and list_tagged[i] == '+':
            list_tagged[i] =  '__PLuS__'
        if list_tagged[i-1] == '/' and list_tagged[i] == '/':
            list_tagged[i-1] = '__SlAsH__'

    string_tageed = "".join(list_tagged)

    temp_tt = string_tageed.split("+")
    temp = []
    if temp_tt:
        temp = temp_tt
    else:
        temp.append(tagged)

    for word in temp:
        temp_1 = word.split("/")
        if temp_1[0] == '__PLuS__':
            temp_1[0] = '+' 
        elif temp_1[0] == '__SlAsH__':
            temp_1[0] = '/'  
        m_tuple = tuple(temp_1)
        result.append(m_tuple)
    return result

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print( "[Usage]", sys.argv[0], "in-file", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1], encoding='utf-8') as fin:

        for line in fin.readlines():

            # 2 column format
            segments = line.split('\t')

            if len(segments) < 2:
                continue

            # result : list of tuples
            result = get_morphs_tags(segments[1].rstrip())

            for morph, tag in result:
                print(morph, tag, sep='\t')
