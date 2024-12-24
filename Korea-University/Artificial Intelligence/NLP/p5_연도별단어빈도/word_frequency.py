#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict
import os
os.chmod("/Users/zs_olef.x/Work/Python/디지털인문학을_위한_데이터처리와분석/assignment5_연도별단어빈도/word_frequency.py", 0o700)

###############################################################################
def word_count(filename):

    word_freq = defaultdict(int)
    #word_freq = dict()
        
    with open( filename, "r", encoding='utf-8') as fin:
        for word in fin.read().split():
            
            word_freq[word] += 1
            
            #if word in word_freq:
            #    word_freq[word] += 1
            #else:
            #    word_freq[word] = 1
    
    return word_freq

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:
        output_file = input_file + ".1gram"
        print( 'processing %s -> %s' %(input_file, output_file), file=sys.stderr)

        word_freq = word_count( input_file)
    
        with open(output_file, "wt", encoding='utf-8') as fout:
            for w, freq in sorted(word_freq.items()):
                print( "%s\t%d" %(w, freq), file=fout)
