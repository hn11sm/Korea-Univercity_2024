with open("sample60.txt", "r") as fp, open("sample60_copy.txt", "r") as fp2, open("sample+-me_file.txt", "w") as fpout:
    for line, line_copy in zip(fp, fp2):
        if line.strip():
            print(line.strip() + " " + line_copy.strip(), file=fpout)
        else:
            print("", file=fpout)