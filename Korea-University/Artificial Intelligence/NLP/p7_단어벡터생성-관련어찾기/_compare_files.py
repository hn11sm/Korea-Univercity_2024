#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import fnmatch
import pickle

def compare_files(year, answer_file, my_file):
    with open(answer_file, 'rb') as f_answer, open(my_file, 'rb') as f_my:
        answer_dict = pickle.load(f_answer)
        my_dict = pickle.load(f_my)
        
        # 딕셔너리 비교
        diff_keys = set(answer_dict.keys()).symmetric_difference(set(my_dict.keys()))
        cnt = 0

        if diff_keys:
            print(f"파일명: {year} - Keys mismatch")
            print(f"Different keys: {diff_keys}")
            cnt += 1
        else:
            # Keys are the same, compare the inner dictionaries
            for key in answer_dict:
                if answer_dict[key] != my_dict[key]:
                    print(f"파일명: {year}, 대상: {key} - Mismatch")
                    print(f"Answer: {answer_dict[key]}")
                    print(f"My file: {my_dict[key]}")
                    cnt += 1
        
        if cnt == 0:
            print(f"파일명: {year} - No error")
        else:
            print(f"파일명: {year} - 오류개수 {cnt}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[Usage]", sys.argv[0], "pattern(s)", file=sys.stderr)
        sys.exit(1)

    file_patterns = sys.argv[1:]

    # 입력 파일들 가져오기
    input_files = []
    for pattern in file_patterns:
        input_files.extend(fnmatch.filter(os.listdir("."), pattern))
    
    # 중복 제거 및 정렬
    input_files = sorted(set(input_files))

    for my_file in input_files:
        year = my_file.split('.')[0]
        answer_file = os.path.join("result", my_file)
        if os.path.exists(answer_file):
            print(f'Processing {year} ({my_file})...')
            compare_files(year, answer_file, my_file)
        else:
            print(f'Answer file for {year} ({my_file}) not found in result directory.')
        print("\n\n")
