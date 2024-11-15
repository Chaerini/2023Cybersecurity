# -*- coding: utf-8 -*-
"""AI보안빅데이터공모전.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oYJTHSm1L5SSLqvI8Bv7Snaee9RQdsaD
"""

# 한글 패치
!sudo apt-get install -y fonts-nanum

!sudo fc-cache -fv

!rm ~/.cache/matplotlib -rf

"""# Sklearn"""

# 구글 드라이브 데이터 불러오기
from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
ai = pd.read_csv('/content/drive/MyDrive/2023AI빅데이터챌린지/A Track 학습셋.csv')
ai.head()

ai = ai[['payload', 'label_action']]
ai

from sklearn.preprocessing import LabelEncoder
labelencoder=LabelEncoder()
for col in ai.columns:
    ai[col] = labelencoder.fit_transform(ai[col])
ai.head()

# x와 y를 분리시킨 후 x를 정규화함.
y = ai['label_action'].values
x = ai.drop(['label_action'], axis=1)
x = x.values
x = (x - x.min()) / (x.max() - x.min())

import matplotlib.pyplot as plt

plt.hist(y)
plt.show()

# 훈련 / 테스트 데이터셋 분리
from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf
x_train , x_test , y_train , y_test = train_test_split(x, y,test_size=0.2,random_state=42)
y_train = tf.keras.utils.to_categorical(y_train, num_classes=9)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=9)

print(x_train.shape, y_train.shape)
print(x_train)
print(y_train)

model = tf.keras.Sequential([
                               tf.keras.layers.Dense(units=48, activation='relu', input_shape=(1,)),
                               tf.keras.layers.Dense(units=24, activation='relu'),
                               tf.keras.layers.Dense(units=12, activation='relu'),
                               tf.keras.layers.Dense(units=9, activation='sigmoid')
])
model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.07),
                loss='binary_crossentropy', metrics=['accuracy'])

model.summary()

print(x_train.shape)

history = model.fit(x_train, y_train, epochs=25, batch_size=32, validation_split=0.25, callbacks=[tf.keras.callbacks.EarlyStopping(patience=3, monitor='val_loss')])

model.evaluate(x_test, y_test)

"""# SVM"""

ai_svm = pd.read_csv('/content/drive/MyDrive/2023AI빅데이터챌린지/A Track 학습셋.csv')
ai_svm.head()

print(ai_svm)

X_train, X_test, y_train, y_test = train_test_split(ai_svm['payload'], ai_svm['label_action'], test_size = 0.2)

print(X_train)

print(y_train)

labelencoder=LabelEncoder()
for col in ai_svm.columns:
    ai_svm[col] = labelencoder.fit_transform(ai_svm[col])
ai_svm.head()

ai_svm = ai_svm[['payload', 'label_action']]

from sklearn.preprocessing import OneHotEncoder

# OneHotEncoder 객체 생성
encoder = OneHotEncoder(sparse=False)  # sparse=False로 설정하여 밀집 배열로 출력

# 데이터를 원-핫 인코딩
ai_svm2 = encoder.fit_transform(ai_svm)

print("원-핫 인코딩 결과:")
print(ai_svm2)

ai_svm2

X_train, X_test, y_train, y_test = train_test_split(ai_svm2['payload'], ai_svm2['label_action'], test_size = 0.2)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
sc.fit(X_train)

X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

"""# 캐글

https://www.kaggle.com/code/dsumarks/2-2-sklearn-and-classifiers-url/notebook
"""

ai_k = pd.read_csv('/content/drive/MyDrive/2023AI빅데이터챌린지/A Track 학습셋.csv')
ai_k.head(15)

plt.figure()

ai_k['label_action'].value_counts().plot(kind='pie', autopct= '%1.0f%%', shadow=True)
plt.title('Types of labels')
plt.show()

# TF-IDF값으로 변환하여 텍스트데이터를 수치화 시킨다.
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(ai_k['payload'])
X.shape

X_train, X_test, y_train, y_test = train_test_split(X, ai_k['label_action'], test_size=0.2, random_state=1337) #Default is test_size = 0.25

#train_sample_size = 1000 #len(X)*0.75
#print(train_sample_size)

print('X_train shape is', X_train.shape)
print('y_train shape is', y_train.shape)
print('X_test shape is', X_test.shape)
print('y_test shape is', y_test.shape)

print(pd.value_counts(y_train))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

#Train sk Model
#model = LogisticRegression()
model = DecisionTreeClassifier()
#model = RandomForestClassifier()

classifier = model.fit(X_train, y_train)
y_pred = model.predict(X_test)
cols = list(classifier.classes_)

import joblib
# Print accuracy:
print("Accuracy: ", accuracy_score(y_test, y_pred))

# 모델저장
joblib.dump(model, 'trained_model.pkl')

import seaborn as sns

ax = plt.subplot()
CM_LR = confusion_matrix(y_test,y_pred)
#sns.heatmap(CM_LR, annot=True, fmt='g', ax=ax)  #annot=True to annotate cells, ftm='g' to disable scientific notation
sns.heatmap(CM_LR, annot=True, fmt = ".1f",cmap="RdBu")
# labels, title and ticks
ax.set_xlabel('Predicted labels')
ax.set_ylabel('True labels')
ax.set_title('Confusion Matrix')
ax.xaxis.set_ticklabels(cols)
ax.yaxis.set_ticklabels(cols)

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

"""# 예선"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier

# 학습 데이터 로드
ai_training = pd.read_csv('/content/drive/MyDrive/2023AI빅데이터챌린지/A Track 학습셋.csv')

# 테스트 데이터 로드
ai_test = pd.read_csv('/content/drive/MyDrive/2023AI빅데이터챌린지/A Track 예선 문제.csv')

# TF-IDF 변환
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(ai_training['payload'])
X_test = vectorizer.transform(ai_test['payload'])

# 학습 데이터의 라벨
y_train = ai_training['label_action']

# 모델 학습
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# 테스트 데이터에 대한 예측
predictions = model.predict(X_test)

# 예측 결과를 테스트 데이터에 추가
ai_test['predictions'] = predictions

# 데이터 확인
ai_test

# ai_test 데이터프레임을 CSV 파일로 저장
ai_test.to_csv('A_Track_할수있조.csv', index=False)