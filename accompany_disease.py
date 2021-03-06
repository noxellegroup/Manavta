import csv
import numpy as np
import pandas as pd
from collections import defaultdict
import ast
import warnings
import joblib
warnings.filterwarnings('ignore')

data1 = pd.read_csv("knowledge.csv")
data1 = pd.DataFrame(data1)
data1.head()

ds1 = data1[["name", "accompany"]]

results = []
for i in ds1['accompany']:
  res = ast.literal_eval(i)
  results.append(res)

ds1['accompanies'] = results

ds1.drop(['accompany'], axis=1)

ds2 = ds1[["name", "accompanies"]]
ds2 = ds2.explode('accompanies')
ds2.size
ds2.head()

unique_diseases = ds2['name'].unique()
print('No. of diseases:', len(unique_diseases))

unique_accompanies = ds2['accompanies'].unique()
print('No. of accompanies', len(unique_accompanies))

df_1 = pd.get_dummies(ds2.accompanies)
df_1.head()

df_s = ds2['name']
df_pivoted = pd.concat([df_s, df_1], axis=1)
df_pivoted.drop_duplicates(keep='first', inplace=True)
df_pivoted = df_pivoted.groupby('name', sort=False).sum()
df_pivoted = df_pivoted.reset_index()
df_pivoted.head()

len(df_pivoted)

x = df_pivoted[df_pivoted.columns[1:]]
y = df_pivoted['name']
df = df_pivoted

X = df.loc[:, df.columns != 'name']
Y = df['name']

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.001, random_state=32)

# Extract features
features = df.columns[1:]

from sklearn.naive_bayes import MultinomialNB
mnb = MultinomialNB()
mnb = mnb.fit(X_train, y_train)

feature_dict = {}
for i,f in enumerate(features):
    feature_dict[f] = i

sample_x = [0] * len(features)
for i in ['pneumonia', 'lung abscess', 'purulent chest', 'pulmonary hypertension', 'chronic pulmonary heart disease']:
    m = feature_dict[i]
    sample_x[m] = 1

# Predicting the Test set results
y_pred = mnb.predict([sample_x])
print(y_pred)

joblib.dump(mnb, 'accompany_disease.joblib')
