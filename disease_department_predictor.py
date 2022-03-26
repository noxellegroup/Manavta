import csv
import numpy as np
import pandas as pd
from collections import defaultdict
import ast
import warnings
import joblib
warnings.filterwarnings('ignore')

def disease_department_predict(symptoms):
    data = pd.read_csv("knowledge.csv")
    data = pd.DataFrame(data)
    data.head()

    ds1 = data[["name", "cure_department"]]

    results = []
    for i in ds1['cure_department']:
        res = ast.literal_eval(i)
        results.append(res)

    ds1['cure_department'] = results

    ds1.drop(['cure_department'], axis=1)

    ds2 = ds1[["name", "cure_department"]]
    ds2 = ds2.explode('cure_department')

    df_1 = pd.get_dummies(ds2.cure_department)

    df_s = ds2['cure_department']
    df_pivoted = pd.concat([df_s, df_1], axis=1)
    df_pivoted.drop_duplicates(keep='first', inplace=True)
    df_pivoted = df_pivoted.groupby('cure_department', sort=False).sum()
    df_pivoted = df_pivoted.reset_index()

    x = df_pivoted[df_pivoted.columns[1:]]
    y = df_pivoted['cure_department']
    df = df_pivoted

    X = df.loc[:, df.columns != 'cure_department']
    Y = df['cure_department']

    # Extract features
    features = df.columns[1:]
    disease_department_model = joblib.load('disease_department.joblib')
    feature_dict = {}
    for i,f in enumerate(features):
        feature_dict[f] = i

    sample_x = [0] * len(features)
    for i in symptoms:
        m = feature_dict[i]
        sample_x[m] = 1
        
    pred = disease_department_model.predict([sample_x])
    return pred[0]