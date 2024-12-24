cnt = 0
line_cnt = 0

with open("sample60.txt", "r") as fp:
    for line in fp:
        line_cnt += 1
        if line.strip("\n") != line.strip():
            cnt+=1
print(cnt)