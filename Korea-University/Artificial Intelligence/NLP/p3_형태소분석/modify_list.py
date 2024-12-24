from konlpy.tag import Mecab
mecab = Mecab()

fp = open("trn.txt", "r")
fp_2 = open("result_mod.txt", "r")
out_fp = open("modify_list.txt", "w")

def compare(str_1, str_2):
    result = []
    if str_1 != str_2:
        result.append(str_1)
        result.append(" ")
        result.append("(")
        temp = str_2.split("\t")
        result.append(temp[1])
        result.append(")")

    return "".join(result)


for line, line2 in zip(fp, fp_2):
    if line.strip() != line2.strip():
        result = compare(line.strip(), line2.strip())
        print(result, file=out_fp)

fp.close()
fp_2.close()
out_fp.close()






