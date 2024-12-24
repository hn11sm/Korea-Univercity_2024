#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import hanja2hangeul_table

h2h_table = hanja2hangeul_table.hanja2hangeul_table

def help(arg):
    print("\n%s Option file(s)"%arg, file=sys.stderr)
    print("\n[Option]", file=sys.stderr)
    print("\t-h1: hangeul", file=sys.stderr)
    print("\t-h2: hangeul(hanja)", file=sys.stderr)
    print("\t-h3: hanja(hangeul)\n", file=sys.stderr)

###############################################################################
# 한자-한글 변환 (문자열 단위; 한자 외 다른 문자들이 포함될 수 있음)
# return value: 한자-한글 변환된 문자열 (형식 1)
# ex) 聖經에 -> 성경에
def hanja2hangeul_str1(str):
    result = []

    for ch in str:
        if ch in h2h_table: 
            result.append(h2h_table[ch][0])
        else:
            result.append(ch)
        
    return ''.join(result)
    
###############################################################################
# 한자-한글 변환 (문자열 단위; 한자 외 다른 문자들이 포함될 수 있음)
# return value: 한자-한글 변환된 문자열 (형식 2)
# ex) 聖經에 -> 성경(聖經)에
def hanja2hangeul_str2(str):
    result = []
    temp = []
        
    for ch in str:
        if ch in h2h_table: 
            result.append(h2h_table[ch][0])
            temp.append(ch)
        else:
            if not temp:
                result.append(ch)
            else:
                result.append("(")
                for tp in temp:
                    result.append(tp)
                result.append(")")
                result.append(ch)
                temp = []
    if temp:
        result.append("(")
        for tp in temp:
            result.append(tp)
        result.append(")")
           
    return ''.join(result)

###############################################################################
# 한자-한글 변환 (문자열 단위; 한자 외 다른 문자들이 포함될 수 있음)
# return value: 한자-한글 변환된 문자열 (형식 3)
# ex) 聖經에 -> 聖經(성경)에
def hanja2hangeul_str3(str):
    result = []
    temp = []
        
    for ch in str:
        if ch in h2h_table: 
            result.append(ch)
            temp.append(h2h_table[ch][0])
        else:
            if not temp:
                result.append(ch)
            else:
                result.append("(")
                for tp in temp:
                    result.append(tp)
                result.append(")")
                result.append(ch)
                temp = []
    if temp:
        result.append("(")
        for tp in temp:
            result.append(tp)
        result.append(")")

    return ''.join(result)

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 3:
        help(sys.argv[0])
        sys.exit()
        
    if sys.argv[1] == '-h1':
        func = hanja2hangeul_str1

    elif sys.argv[1] == '-h2':
        func = hanja2hangeul_str2

    elif sys.argv[1] == '-h3':
        func = hanja2hangeul_str3

    else:
        help(sys.argv[0])
        sys.exit()
        
    for filename in sys.argv[2:]:

        try:
            fp = open(filename, "r")
        except:
            print("File open error:", filename, file=sys.stderr)
        try:
            outfp = open(filename+".out", "w")
        except:
            print("File open error:", filename+".out", file=sys.stderr)

        print("%s -> %s"%(filename, filename+".out"), file=sys.stderr)

        for line in fp:
            
            result = func(line.rstrip())
            
            print(result, file=outfp)
        
        fp.close()
        outfp.close()
