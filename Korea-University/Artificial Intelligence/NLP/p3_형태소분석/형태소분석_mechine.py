from konlpy.tag import Okt
from sklearn_crfsuite import CRF

# 파일에서 학습 데이터 읽어오기
def read_training_data(file_path):
    training_data = []
    with open('train.txt', 'r', encoding='utf-8') as file:
        for line in file:
            sentence, tags = line.strip().split(' ')
            training_data.append((sentence, tags))
    return training_data

# 형태소 분석기 초기화
okt = Okt()

# 파일에서 학습 데이터 읽어오기
training_data = read_training_data('training_data.txt')

# 학습 데이터를 형태소와 태그로 분리
X_train = [okt.morphs(sentence) for sentence, _ in training_data]
y_train = [tags.split('+') for _, tags in training_data]

# 형태소와 태그를 고유한 정수로 매핑
morphemes = sum(X_train, [])
tags = sum(y_train, [])

morphemes_vocab = {morph: idx for idx, morph in enumerate(set(morphemes))}
tags_vocab = {tag: idx for idx, tag in enumerate(set(tags))}

# 학습 데이터를 정수로 변환
X_train_int = [[morphemes_vocab[m] for m in sent] for sent in X_train]
y_train_int = [[tags_vocab[t] for t in tags] for tags in y_train]

# CRF 모델 학습
crf = CRF()
crf.fit(X_train_int, y_train_int)

# 형태소 분석 함수 정의
def pos_tagging(sentence):
    morphs = okt.morphs(sentence)
    morphs_int = [morphemes_vocab.get(m, 0) for m in morphs]
    tags_int = crf.predict_single(morphs_int)
    tags = [list(tags_vocab.keys())[idx] for idx in tags_int]
    return list(zip(morphs, tags))

# 새로운 문장에 대한 형태소 분석 수행
new_sentence = "기자가 요즘의 대표번호로 휴대전화로도 이렇게 포스팅이 된다니."
result = pos_tagging(new_sentence)
print(result)
