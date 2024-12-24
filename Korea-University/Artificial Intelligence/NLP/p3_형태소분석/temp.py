from konlpy.tag import Mecab
mecab = Mecab()

fp = open("trn.txt", "r")
fpout = open("trn_sample.txt", "w")

def divide(str):

    result = str.split("\t")

    return result[0]


for line in fp:
    result = divide(line.strip())
    print(result, file=fpout)

fp.close()
fpout.close()






