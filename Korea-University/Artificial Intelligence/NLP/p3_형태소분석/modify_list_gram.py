from konlpy.tag import Mecab
mecab = Mecab()

fp = open("trn.txt", "r")
fp_2 = open("result_mod.txt", "r")
out_fp = open("modify_list_gram.txt", "w")

def compare(str_1, str_2):
    result = []
    result.append(str_1)
    result.append(" ")
    result.append("(")
    temp = str_2.split("\t")
    result.append(temp[1])
    result.append(")")

    return "".join(result)


for line, line2 in zip(fp, fp_2):
    if line.strip() != line2.strip():
        str1_list = line.strip().split("+")
        str1_len = len(str1_list)
        str2_list = line2.strip().split("+")
        str2_len = len(str2_list)
        result_1 = []
        for word in str1_list:
            temp = word.split("/")
            result_1.append(temp[0])
        result_2 = []
        for word in str2_list:
            temp = word.split("/")
            result_2.append(temp[0])
        if str1_len == str2_len and result_1 == result_2:
            result = compare(line.strip(), line2.strip())
            print(result, file=out_fp)

fp.close()
fp_2.close()
out_fp.close()






