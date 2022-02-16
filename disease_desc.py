import pandas as pd
import openpyxl
import xlsxwriter
import numpy as np
import scipy
from sentence_transformers import SentenceTransformer

def disease_desc_display(problem):
    df = pd.ExcelFile('description.xlsx')
    df = df.parse('description')
    df.dropna(inplace=True, axis=0)

    diseases = list(df['Disease'])

    if problem in diseases:
        return df['Description'][diseases.index(problem)]
    else:
        # Optimization needed for this
        model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
        diseases_embeddings = model.encode(diseases)
        diseases_embeddings.shape

        problem_embedding = model.encode(problem)

        np.round(1-scipy.spatial.distance.cdist([problem_embedding], diseases_embeddings[:4,:], "cosine"), 2)

        similarities = np.round(1-scipy.spatial.distance.cdist([problem_embedding], diseases_embeddings, "cosine"), 2)
        similarities = similarities.flatten()
        similarities_desc = np.sort(similarities)[::-1]

        indexes = np.array([i for i in range(diseases_embeddings.shape[0])])
        best_matches = indexes[np.argsort(similarities)[::-1]]

        topn = 1
        for i in range(topn):
            return df['Description'][best_matches[i]]
        
