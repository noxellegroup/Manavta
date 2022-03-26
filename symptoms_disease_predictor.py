import csv
import numpy as np
import pandas as pd
from collections import defaultdict
import ast
import warnings
import joblib
warnings.filterwarnings('ignore')

def symptoms_disease_predict(symptoms):
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

    ds2 = ds1[["name", "symptoms"]]
    ds2 = ds2.explode('symptoms')

    df_1 = pd.get_dummies(ds2.symptoms)

    df_s = ds2['name']
    df_pivoted = pd.concat([df_s, df_1], axis=1)
    df_pivoted.drop_duplicates(keep='first', inplace=True)
    df_pivoted = df_pivoted.groupby('name', sort=False).sum()
    df_pivoted = df_pivoted.reset_index()

    x = df_pivoted[df_pivoted.columns[1:]]
    y = df_pivoted['name']
    df = df_pivoted

    X = df.loc[:, df.columns != 'name']
    Y = df['name']

    # Extract features
    features = df.columns[1:]
    symptoms_disease_model = joblib.load('symptoms_disease.joblib')
    feature_dict = {}
    for i,f in enumerate(features):
        feature_dict[f] = i

    sample_x = [0] * len(features)
    for i in symptoms:
        m = feature_dict[i]
        sample_x[m] = 1
        
    pred = symptoms_disease_model.predict([sample_x])
    return pred[0]