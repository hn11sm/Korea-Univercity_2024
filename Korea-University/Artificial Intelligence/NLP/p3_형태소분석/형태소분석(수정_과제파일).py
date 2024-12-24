from konlpy.tag import Mecab
mecab = Mecab()

def modify(stemming_list, stemming_list_ori):
    result = []
    for entry in stemming_list:
        temp = []
        temp.append(entry[0])
        temp.append(entry[1])
        if entry[1] == 'SSO':
            temp[1] = 'SS' 
        elif entry[1] == 'SSC':
            temp[1] = 'SS'
        elif entry[1] == 'SSC':
            temp[1] = 'SS'
        elif entry[1] == 'SY':
            temp[1] = 'SS'
        elif entry[1] == 'SC':
            temp[1] = 'SP'
        elif entry[1] == 'EF':
            temp[1] = 'EM'
        elif entry[1] == 'EC':
            temp[1] = 'EM'
        elif entry[1] == 'JC':
            temp[1] = 'JKB'
        elif entry[1] == 'VCN':
            temp[1] = 'VCP'
        elif entry[1] == 'NF':
            temp[1] = 'NA'
        elif entry[1] == 'XR':
            temp[1] = 'NNG'
        elif entry[1] == 'NAP':
            temp[1] = 'NNP'
        elif entry[1] == 'JKC':
            temp[1] = 'JKS'
        elif entry[1] == 'MMA' or entry[1] == 'MMD' or entry[1] == 'MMN':
            temp[1] = 'MM'
        elif entry[1] == 'NNBC':
            temp[1] = 'NNB'
        result.append(temp)
    
    result_2 = []
    for entry in stemming_list_ori:
        temp = []
        temp.append(entry[0])
        temp.append(entry[1])
        if entry[1] == 'SSO':
            temp[1] = 'SS' 
        elif entry[1] == 'SSC':
            temp[1] = 'SS'
        elif entry[1] == 'SSC':
            temp[1] = 'SS'
        elif entry[1] == 'SY':
            temp[1] = 'SS'
        elif entry[1] == 'SC':
            temp[1] = 'SP'
        elif entry[1] == 'EF':
            temp[1] = 'EM'
        elif entry[1] == 'EC':
            temp[1] = 'EM'
        elif entry[1] == 'JC':
            temp[1] = 'JKB'
        elif entry[1] == 'VCN':
            temp[1] = 'VCP'
        elif entry[1] == 'NF':
            temp[1] = 'NA'
        elif entry[1] == 'XR':
            temp[1] = 'NNG'
        elif entry[1] == 'NAP':
            temp[1] = 'NNP'
        elif entry[1] == 'JKC':
            temp[1] = 'JKS'
        elif entry[1] == 'MMA' or entry[1] == 'MMD' or entry[1] == 'MMN':
            temp[1] = 'MM'
        elif entry[1] == 'NNBC':
            temp[1] = 'NNB'
        result_2.append(temp)

    return result, result_2

def compare(t, t_ori):
    for word, word_ori in zip(t, t_ori):
        if word[1] != word_ori[1]:
            word_ori[1] = word[1]
    return t_ori


def stemming(str, str_ori):
    result = []

    temp = mecab.pos(str)
    temp_ori = mecab.pos(str_ori)

    t, t_ori = modify(temp, temp_ori)
    token = compare(t, t_ori)

    result.append(str_ori)
    if str_ori != "":
        result.append("\t")
    length_ori = len(token)
    idx = 0

    for word in token:
        idx += 1
        result.append(word[0])
        result.append("/")
        result.append(word[1])
        if idx != length_ori:
            result.append("+")

    
    return ''.join(result)

with open("sample55+-.txt", "r") as fp, open("sample55.txt", "r") as fp2, open("sample_output.txt", "w") as outfp:
    temp = []
    # 두 줄씩 형태소 분석 후 출력
    for line, line_ori in zip(fp, fp2):
        line1 = line.rstrip()
        line2_ori = line_ori.rstrip()
        result = stemming(line1, line2_ori)
        print(result, file=outfp)
