from konlpy.tag import Mecab
mecab = Mecab()

def modify(stemming_list):
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
        elif entry[1] == 'NNBC':
            temp[1] = 'NNB'
        elif entry[1] == 'VA':
            temp[1] = 'VX'
        result.append(temp)
    return result

def stemming(str):
    result = []
    temp = mecab.pos(str)
    token = modify(temp)
    result.append(str)
    result.append("\t")
    length = len(token)
    idx = 0
    for word in token:
        idx += 1
        result.append(word[0])
        result.append("/")
        result.append(word[1])
        if idx != length:
            result.append("+")

    
    return ''.join(result)

with open("trn_sample.txt", "r") as fp, open("result_sample.txt", "w") as outfp:
    lines = fp.readlines() 
    
    # 두 줄씩 형태소 분석 후 출력
    for i in range(0, len(lines)):
        line1 = lines[i].rstrip()
        result = stemming(line1)
        print(result, file=outfp)
