#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import fnmatch

def compare_files(year, answer_file, my_file):
    with open(answer_file, 'r', encoding='utf-8') as f_answer, open(my_file, 'r', encoding='utf-8') as f_my:
        answer_lines = f_answer.readlines()
        my_lines = f_my.readlines()
        
        # 파일의 각 줄을 비교하고 다른 줄의 인덱스를 저장
        diff_indices = [i for i, (answer_line, my_line) in enumerate(zip(answer_lines, my_lines)) if answer_line != my_line]
        
        # 다른 줄이 있다면 해당 줄을 출력
        cnt = 0
        if diff_indices:
            for idx in diff_indices:
                print(f"Year: {year}, 위치: {idx + 1} 번째 줄")
                print(f"Answer: {answer_lines[idx].strip()}, My file: {my_lines[idx].strip()}")
                cnt += 1
                error = f'{year}'
        else:
            print(f"Year: {year} - No error")
        print(f"Year: {year} - 오류개수 {cnt}")

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
