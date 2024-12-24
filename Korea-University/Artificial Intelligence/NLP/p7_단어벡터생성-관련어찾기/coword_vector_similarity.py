#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pickle
import math # sqrt

###############################################################################
def cosine_similarity(t_vector, c_vector):
    common_keys = set(t_vector.keys()) & set(c_vector.keys())

    dot_product = sum(t_vector[key] * c_vector[key] for key in common_keys)

    magnitude_t_vector = math.sqrt(sum(value ** 2 for value in t_vector.values()))
    
    magnitude_c_vector = math.sqrt(sum(value ** 2 for value in c_vector.values()))
    
    if magnitude_t_vector == 0 or magnitude_c_vector == 0:
        return 0.0
    else:
        return dot_product / (magnitude_t_vector * magnitude_c_vector)


###############################################################################
def most_similar_words(word_vectors, target, topN=10):
    result = {} 
    
    if target not in word_vectors:
        return result

    target_vector = word_vectors[target]
    candidates = set(target_vector.keys()) 

    for co_word in target_vector:
        if co_word in word_vectors:
            candidates.update(word_vectors[co_word].keys())

    for word in candidates:
        if word == target or word in target:
            continue
        
        if word in word_vectors:
            similarity = cosine_similarity(target_vector, word_vectors[word])
            if similarity > 0.001:
                result[word] = similarity

    return sorted(result.items(), key=lambda x: x[1], reverse=True)[:topN]

###############################################################################
def print_words(words):
    for word, score in words:
        print("%s\t%.3f" %(word, score))
    
###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print( "[Usage]", sys.argv[0], "in-file(pickle)", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1],"rb") as fin:
        word_vectors = pickle.load(fin)

    while True:

        print('\n검색할 단어를 입력하세요(type "^D" to exit): ', file=sys.stderr)
    
        try:
            query = input()
            
        except EOFError:
            print('프로그램을 종료합니다.', file=sys.stderr)
            break
    
        # result : list of tuples, sorted by cosine similarity
        result = most_similar_words(word_vectors, query, topN=30)
        
        if result:
            print_words(result)
        else:
            print('\n결과가 없습니다.')
