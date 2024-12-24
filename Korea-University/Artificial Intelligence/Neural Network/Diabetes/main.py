import os
print(os.getcwd())
import matplotlib
matplotlib.use("TkAgg")
from utils import preprocess
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_curve, accuracy_score
from keras.models import Sequential
from keras.layers import Dense, Dropout
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)  # Seed 값 변경

try:
    df = pd.read_csv('Diabetes/diabetes.csv')
except FileNotFoundError:
    print("Dataset not found in your computer.")
    quit()

df = preprocess(df)

# Split the data into a training and testing set
X = df.drop(columns=['Outcome'])  # X에 사용하는 데이터를 더 명확히 지정
y = df['Outcome']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Sequential()
model.add(Dense(64, activation='relu', input_dim=X_train.shape[1]))  # 은닉 노드 증가
model.add(Dropout(0.2)) 
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.2)) 
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=100, verbose=False, validation_split=0.2)

# Results - Accuracy
train_accuracy = model.evaluate(X_train, y_train, verbose=False)[1]
test_accuracy = model.evaluate(X_test, y_test, verbose=False)[1]
print("Training Accuracy: %.2f%%" % (train_accuracy * 100))
print("Testing Accuracy: %.2f%%" % (test_accuracy * 100))

# Results - Confusion Matrix
y_test_pred_probs = model.predict(X_test)
y_test_pred = (y_test_pred_probs > 0.5).astype(int)  # Threshold는 여전히 0.5
c_matrix = confusion_matrix(y_test, y_test_pred)
sns.heatmap(c_matrix, annot=True, fmt='d', xticklabels=['No Diabetes', 'Diabetes'], yticklabels=['No Diabetes', 'Diabetes'], cmap='Blues')
plt.xlabel("Prediction")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# Results - ROC Curve
FPR, TPR, _ = roc_curve(y_test, y_test_pred_probs)
plt.plot(FPR, TPR, label='ROC Curve')
plt.plot([0, 1], [0, 1], 'k--', label='Random Guess')
plt.title('ROC Curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.show()