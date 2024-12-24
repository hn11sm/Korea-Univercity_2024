#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict
from itertools import combinations

###############################################################################
def print_word_freq(filename, word_freq):
    with open(filename, "wt", encoding='utf-8') as fout:
            for w, freq in sorted(word_freq.items()):
                print( "%s\t%d" %(w, freq), file=fout)



###############################################################################
def get_coword_freq(filename):
    word_freq = defaultdict(int)
    coword_freq = defaultdict(int)
    word_context_size = defaultdict(int)
    #word_freq = dict()
        
    with open(filename, "r", encoding='utf-8') as fin:
        total = 0
        lines = fin.readlines()
        for line in lines:
            if line.strip():
                sentence = line.strip()
                words = sentence.split()
                set_word_list = set(words)
                for word in set_word_list:
                    word_freq[word] += 1
                    word_context_size[word] += len(set_word_list)
                    total += 1
        word_freq['#Total'] = total

    with open(filename, "r", encoding='utf-8') as fin:
        lines = fin.readlines()
        for line in lines:
            if line.strip():
                sentence = line.strip()
                words = sentence.split()
                set_word_list = set(words)
                for target, coword in combinations(set_word_list, 2):
                    if target < coword:
                        temp = target + '\t' + coword
                    else:
                        temp = coword + '\t' + target
                    coword_freq[temp] += 1
        
    return word_freq, coword_freq, word_context_size

###############################################################################
def print_coword_freq(filename, coword_freq):
    with open(filename, "wt", encoding='utf-8') as fout:
            for cow, freq in sorted(coword_freq.items()):
                print( "%s\t%d" %(cow, freq), file=fout)




###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:
        
        print( 'processing %s' %input_file, file=sys.stderr)
        
        file_stem = input_file
        pos = input_file.find(".")
        if pos != -1:
            file_stem = input_file[:pos] # ex) "2017.tag.context" -> "2017"
        
        # 1gram, 2gram, 1gram context 빈도를 알아냄
        word_freq, coword_freq, word_context_size = get_coword_freq(input_file)

        # unigram 출력
        print_word_freq(file_stem+".1gram", word_freq)
        
        # bigram(co-word) 출력
        print_coword_freq(file_stem+".2gram", coword_freq)

        # unigram context 출력
        print_word_freq(file_stem+".1gram_context", word_context_size)
