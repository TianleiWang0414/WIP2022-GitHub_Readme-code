import json
import pandas as pd



from scipy.stats import ranksums
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance, PartialDependenceDisplay
from sklearn.model_selection import train_test_split, cross_val_score, KFold, cross_validate
from sklearn.preprocessing import LabelBinarizer, OneHotEncoder
from sklearn.pipeline import Pipeline
import numpy as np
from numpy.random import normal
from sklearn.impute import SimpleImputer

"""
This file is responsible for generating p value info for feature importance

Run following to get the required data:
data_retrieval_README_attr.py
data_retrieval_meta_data.py
data_retrieval_commits.py
topic_points.py
header_to_feature.py
time_based.py
"""


def initial(file_name: str):
    data = pd.read_csv(file_name,
                       usecols=['name', 'user', 'readme', 'star', 'blocks', 'indents', 'images', 'links', 'lists',
                                'language',
                                'license', 'readme_length', 'topic_score_average', 'update_interval', 'prob_popular',
                                'label', 'badge_count', 'Number_of_update', 'repo_size'])

    data['language'].fillna('None_language', inplace=True)
    data['license'].fillna('None_license', inplace=True)
    print(len(data))
    language_encoder = OneHotEncoder(handle_unknown="ignore")
    license_encoder = OneHotEncoder(handle_unknown="ignore")
    numerical_pipe = Pipeline([("imputer", SimpleImputer(strategy="mean"))])
    preprocessing = ColumnTransformer(
        [
            ("language", language_encoder, ['language']),
            ("license", license_encoder, ['license']),
            ("nums", numerical_pipe,
             ['blocks', 'indents', 'images', 'links', 'lists', 'readme_length', 'topic_score_average',
              'update_interval', 'prob_popular', 'badge_count', 'Number_of_update', 'repo_size']),
        ]
    )

    new_data = data.sample(frac=1).reset_index(drop=True)  # shuffle
    print(new_data)
    _y_train = new_data['label']
    _X_train = new_data.drop(['label'], axis=1)

    _X_train = _X_train.drop(['star', 'name', 'user', 'readme'], axis=1)

    print(len(_X_train))
    rf = Pipeline(
        [
            ("preprocess", preprocessing),
            ("classifier", RandomForestClassifier(n_estimators=200)),
        ]
    )
    total_res = []
    for _ in range(100):
        total_res.append([])
    length = 0
    print(list(_X_train.columns))
    for _ in range(100):
        X_train, X_test, y_train, y_test = train_test_split(
            _X_train, _y_train,
            test_size=0.1)
        col = X_test.columns
        rf.fit(X_train, y_train)
        result = permutation_importance(
            rf, X_test, y_test, n_repeats=10, random_state=42, n_jobs=2, scoring='r2'
        )

        if length == 0:
            length = len(result.importances_mean)
            print(length)
        arr = list(result.importances_mean)
        print(arr)
        for i in range(length):
            value = arr[i]
            total_res[i].append(value)

    key_value = {}

    for i in range(length):
        print(total_res[i])
        key_value[list(_X_train.columns)[i]] = total_res[i]

    with open('p_value.json', 'w') as f:
        json.dump(key_value, f)


if __name__ == '__main__':
    __file_name = ""
    initial(__file_name)

    # print p-value stats
    with open('p_value.json', 'r') as f:
        data = json.load(f)
    a = normal(loc=0, scale=0, size=100)
    for k, v in data.items():
        result = str(ranksums(list(a), v).pvalue)
        message = k + " p = " + result
        print(message)
        print(k + " Median %f" % np.median(v))
