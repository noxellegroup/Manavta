import csv
import numpy as np
import pandas as pd
from collections import defaultdict
import ast
import warnings
import joblib
warnings.filterwarnings('ignore')

data = pd.read_csv("knowledge.csv")
data = pd.DataFrame(data)
data.head()

ds1 = data[["name", "symptom"]]

results = []
for i in ds1['symptom']:
    res = ast.literal_eval(i)
    results.append(res)

ds1['symptoms'] = results

ds1.drop(['symptom'], axis=1)

ds2=ds1[["name", "symptoms"]]
ds2 = ds2.explode('symptoms')
ds2.size
ds2.head()

unique_diseases = ds2['name'].unique()
print('No. of diseases:', len(unique_diseases))

unique_symptoms = ds2['symptoms'].unique()
print('No. of symptoms', len(unique_symptoms))

df_1 = pd.get_dummies(ds2.symptoms)
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

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30, random_state=32)

# Extract features
features = df.columns[1:]

# Multinomial Naive Bayes
from sklearn.naive_bayes import MultinomialNB
mnb = MultinomialNB()
mnb = mnb.fit(X_train, y_train)

feature_dict = {}
for i,f in enumerate(features):
    feature_dict[f] = i

sample_x = [0] * len(features)
for i in ['night sweats', 'diarrhea', 'fever with cough']:
    m = feature_dict[i]
    sample_x[m] = 1

# Predicting the Test set results
y_pred = mnb.predict([sample_x])
print(y_pred)

# Saving the model
joblib.dump(mnb, 'symptoms_disease.joblib')