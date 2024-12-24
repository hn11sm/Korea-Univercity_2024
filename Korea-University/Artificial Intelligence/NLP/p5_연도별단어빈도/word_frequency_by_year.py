#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict

###############################################################################
def word_count(filename):
    word_freq = defaultdict(int)
    
    with open(filename, "r", encoding='utf-8') as fin:
        for word in fin.read().split():
            word_freq[word] += 1
    
    return word_freq

def update_dictionary(word_counts, idx, word_counts_by_year):
    len_list = []

    for word, count in word_counts_by_year.items():
        if word in word_counts:
            word_counts[word].append(count)
        else:
            word_counts[word] = [0] * idx
            word_counts[word].append(count)

    for _, freq_list in word_counts.items():
        len_list.append(len(freq_list))

    max_len = max(len_list)

    for word, _ in word_counts.items():
        if len(word_counts[word]) < max_len:
            for i in range(0, max_len-len(word_counts[word])):
                word_counts[word].append(0)
                
    return word_counts

###############################################################################
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    word_freq_years = {}
    idx = 0

    for input_file in sys.argv[1:]:
        idx += 1
        word_dic = word_count(input_file)
        word_freq_years = update_dictionary(word_freq_years, idx, word_dic)
    
    for word, value in word_freq_years.items():
        word_freq_years[word] = value[1:]

    for w, freq in sorted(word_freq_years.items()):
        print("%s\t%s" % (w, freq), encoding='utf-8')
