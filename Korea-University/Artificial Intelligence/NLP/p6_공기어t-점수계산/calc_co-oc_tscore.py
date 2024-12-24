#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math # sqrt

###############################################################################
def read_frequency(filename):
    freqs = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            tokens = line.strip().split('\t')
            if tokens[0] == "#Total":
                freqs['#Total'] = int(tokens[1])
            else:
                freqs[tokens[0]] = int(tokens[1])
    return freqs

###############################################################################
def calc_tscore(filename, unigrams, unigram_context, uni_N, cutoff):
    t_scores = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            target, collocate, freq = line.strip().split('\t')
            freq = int(freq)
            if freq >= cutoff:
                if target in unigrams and collocate in unigrams and collocate in unigram_context:
                    O = freq
                    E = (unigram_context[target] * unigrams[collocate]) / uni_N
                    if O > 0 and E > 0:
                        t_score = (O - E) / math.sqrt(O)
                        if t_score > 0:
                            t_scores.append((target, collocate, t_score))
                    
                    O_reversed = freq
                    E_reversed = (unigram_context[collocate] * unigrams[target]) / uni_N
                    if O_reversed > 0 and E_reversed > 0:
                        t_score_reversed = (O_reversed - E_reversed) / math.sqrt(O_reversed)
                        if t_score_reversed > 0:
                            t_scores.append((collocate, target, t_score_reversed))
    
    t_scores = [
        (target, collocate, t_score) for target, collocate, t_score in t_scores
        if not (collocate in target)
    ]

    return t_scores

###############################################################################
def print_tscore(filename, t_scores):   
    with open(filename, 'w', encoding='utf-8') as file:
        for target, collocate, t_score in sorted(t_scores, key=lambda x: (x[0], x[1])):
            file.write(f"{target}\t{collocate}\t{t_score:.3f}\n")

###############################################################################
if __name__ == "__main__":

    CUTOFF = 5 # 공기빈도가 이 값 이상인 경우만 t점수를 계산
    
    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:
        
        print( 'processing %s' %input_file, file=sys.stderr)

        file_stem = input_file
        pos = input_file.find(".")
        if pos != -1:
            file_stem = input_file[:pos] # ex) "2017.2gram" -> "2017"
    
        print("\tLoading %s.1gram" %file_stem, file=sys.stderr)
        unigrams = read_frequency(file_stem+".1gram")
        
        print("\tLoading %s.1gram_context" %file_stem, file=sys.stderr)
        unigram_context = read_frequency(file_stem+".1gram_context")
        
        uni_N = unigrams['#Total'] # unigram 빈도 합
        
        t_scores = calc_tscore(input_file, unigrams, unigram_context, uni_N, CUTOFF)
        
        print_tscore(file_stem+".tscore", t_scores)

