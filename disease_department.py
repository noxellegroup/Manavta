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

ds1 = data1[["name", "cure_department"]]

results = []
for i in ds1['cure_department']:
  res = ast.literal_eval(i)
  results.append(res)

ds1['cure_departments'] = results

ds1.drop(['cure_department'], axis=1)

ds2=ds1[["name", "cure_departments"]]
ds2 = ds2.explode('cure_departments')
ds2.size
ds2.head()

unique_diseases = ds2['name'].unique()
print('No. of diseases:', len(unique_diseases))

unique_departments = ds2['cure_departments'].unique()
print('No. of departments', len(unique_departments))

df_1 = pd.get_dummies(ds2.name)
df_1.head()

df_s = ds2['cure_departments']
df_pivoted = pd.concat([df_s, df_1], axis=1)
df_pivoted.drop_duplicates(keep='first', inplace=True)
df_pivoted = df_pivoted.groupby('cure_departments', sort=False).sum()
df_pivoted = df_pivoted.reset_index()
df_pivoted.head()

len(df_pivoted)



x = df_pivoted[df_pivoted.columns[1:]]
y = df_pivoted['cure_departments']
df = df_pivoted

X = df.loc[:, df.columns != 'cure_departments']
Y = df['cure_departments']

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
for i in ['asthmatic bronchitis']:
    m = feature_dict[i]
    sample_x[m] = 1

# Predicting the Test set results
y_pred = mnb.predict([sample_x])
print(y_pred)

joblib.dump(mnb, 'disease_department.joblib')