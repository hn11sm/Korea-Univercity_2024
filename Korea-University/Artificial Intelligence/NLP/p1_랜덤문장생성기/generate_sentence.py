#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
os.chmod('/Users/zs_olef.x/data/assignment1_랜덤문장생성기/generate_sentence.py', 0o700)

import sys
import pickle
import random # choice

def generate_sentence(bigrams, start_with='<s>'):
    end_sign = '</s>'
    sentence = []
    start_words = start_with.split()
    
    if all(word in bigrams for word in start_woåårds):
        current_word = start_words[-1]
    else:
        print("시작 단어(들) '{}'가 학습 데이터에 존재하지 않습니다.".format(start_with))
        quit()
    
    sentence = [start_with]

    while True:
        next_word_values = bigrams.get(current_word, [])
        if not next_word_values:
            break
        next_word = random.choice(next_word_values)
        if next_word == end_sign:
            break
        if next_word != end_sign:
            sentence.append(next_word)
        current_word = next_word

    print(' '.join(sentence))

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print( "[Usage] %s in-file(pickle)" %sys.argv[0], file=sys.stderr)
        sys.exit()

    with open(sys.argv[1],"rb") as fp:
        bigrams = pickle.load(fp)

    for i in range(10):
        print(i, end=' : ')
        generate_sentence(bigrams, "나는 언제나")
        print()
