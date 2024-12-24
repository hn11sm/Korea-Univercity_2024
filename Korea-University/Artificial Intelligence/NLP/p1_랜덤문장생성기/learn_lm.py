#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import pickle
 
def learn_lm(filename):
    bigrams = {}
    end_sign = '</s>'
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                sentence = line.strip() + ' ' + end_sign
                words = sentence.split()
                for i in range(len(words) - 1):
                    current_word = words[i]
                    next_word = words[i + 1]
                    if current_word not in bigrams:
                        bigrams[current_word] = []
                    if next_word not in bigrams[current_word]:
                        bigrams[current_word].append(next_word)
    return bigrams

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print( "[Usage] %s in-file out-file(pickle)" %sys.argv[0], file=sys.stderr)
        sys.exit()

    filename = sys.argv[1]
    print("processing %s ..." %filename, file=sys.stderr)
    
    bigrams = learn_lm(filename)

    with open(sys.argv[2],"wb") as fout:
        print("saving %s" %sys.argv[2], file=sys.stderr)
        pickle.dump(bigrams, fout)
