def compare_files(answer_file, my_file):
    with open(answer_file, 'r', encoding='utf-8') as f_answer, open(my_file, 'r', encoding='utf-8') as f_my:
        answer_lines = f_answer.readlines()
        my_lines = f_my.readlines()
        
        # 파일의 각 줄을 비교하고 다른 줄의 인덱스를 저장
        diff_indices = [i for i, (answer_line, my_line) in enumerate(zip(answer_lines, my_lines)) if answer_line != my_line]
        
        # 다른 줄이 있다면 해당 줄을 출력
        if diff_indices:
            for idx in diff_indices:
                print(f"Answer: {answer_lines[idx].strip()}, My file: {my_lines[idx].strip()} 위치: {idx+1} 번째 줄")
        else:
            print("No error")
 
# 파일 경로 설정
answer_file = "/Users/zs_olef.x/Work/Python/디지털인문학을_위한_데이터처리와분석/assignment4_형태소품사색인어추출/all.tag.context_copy"
my_file = "/Users/zs_olef.x/Work/Python/디지털인문학을_위한_데이터처리와분석/assignment4_형태소품사색인어추출/all.tag.context"

# 파일 비교 함수 호출
compare_files(answer_file, my_file)
