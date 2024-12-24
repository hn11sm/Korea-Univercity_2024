#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import get_morphs_tags as mf



###############################################################################
# 색인어 (명사, 복합명사 등) 추출
def get_index_terms(mt_list):
    nouns = []
    compound_nouns = []
    is_compound = False
    idx_SL_list = []
    idx = -1
    for word, pos in mt_list:
        if pos in ['NNG', 'NNP', 'SL', 'SH']:
            nouns.append(word)
            idx+=1
            if pos == 'SL':
                idx_SL_list.append(idx)

            compound_nouns.append(word)
            is_compound = True
        elif pos in ['NR', 'NNB', 'SN']:
            compound_nouns.append(word)
            is_compound = True
        else:
            if is_compound == True and len(compound_nouns) >= 2:
                nouns.append("".join(compound_nouns))
                for i in range(len(idx_SL_list)-1, -1, -1):
                    del nouns[idx_SL_list[i]]
                    idx-=1
                idx+=1
                idx_SL_list = []
                compound_nouns = []
                is_compound = False
            else:
                idx_SL_list = []
                compound_nouns = []
                is_compound = False

    if is_compound == True and len(compound_nouns) >= 2:
        for i in range(len(idx_SL_list)-1, -1, -1):
            del nouns[idx_SL_list[i]]
        nouns.append("".join(compound_nouns))

    return nouns
###############################################################################
# Converting POS tagged corpus to a context file
def tagged2context( input_file, output_file):
    try:
        fin = open( input_file, "r", encoding='utf-8')
    except:
        print( "File open error: ", input_file, file=sys.stderr)
        sys.exit()

    try:
        fout = open( output_file, "w", encoding='utf-8')
    except:
        print( "File open error: ", output_file, file=sys.stderr)
        sys.exit()

    for line in fin.readlines():

        # 빈 라인 (문장 경계)
        if line[0] == '\n':
            print("", file=fout)
            continue

        try:
            ej, tagged = line.split(sep='\t')
        except:
            print(line, file=sys.stderr)
            continue

        # 형태소, 품사 추출
        # result : list of tuples
        result = mf.get_morphs_tags(tagged.rstrip())

        # 색인어 추출
        terms = get_index_terms(result)

        # 색인어 출력
        for term in terms:
            print(term, end=" ", file=fout)

    fin.close()
    fout.close()

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:
        output_file = input_file + ".context"
        print( 'processing %s -> %s' %(input_file, output_file), file=sys.stderr)

        # 형태소 분석 파일 -> 문맥 파일
        tagged2context( input_file, output_file)
