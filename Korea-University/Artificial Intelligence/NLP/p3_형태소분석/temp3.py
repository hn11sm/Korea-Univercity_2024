from konlpy.tag import Mecab
mecab = Mecab()

temp = mecab.pos("민감 한")

print(temp)

if "\"" == "”":
    print(True)
else:
    print(False)

# 세단어 연속으로 분석
# ㅇ+ㅇ 나누기
# ㄴ 예외처리
#해야	하/XSV+아야/EM
#해진 하/XSA+아/EM+지/VX+ㄴ/ETM
#끌어와	끌어오/VV+아/EM
#라는 이/VCP+라는/ETM
#이뤄지진	이뤄지/VV+지/EM+ㄴ/JX -> 오류
# 야후스포츠는	야후/NNP+스포츠/NNP+는/JX 
# 야후스포츠는	야후스포츠/NNP+는/JX
