with open("sample55.txt", "r") as fp, open("sample55_copy.txt", "r") as fp2, open("sample55+-.txt", "w") as fpout:
    for line, line_copy in zip(fp, fp2):
        if line.strip():
            print(line.strip() + " " + line_copy.strip(), file=fpout)
        else:
            print("", file=fpout)