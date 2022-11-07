import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance, PartialDependenceDisplay
from sklearn.model_selection import train_test_split, cross_val_score, KFold, cross_validate
from sklearn.preprocessing import LabelBinarizer, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from datetime import date

from RQ2.RQ2_util.split_popular import get_non_popular, get_popular

"""
This file is responsible for the feature importance feature, and create Random Forest PDP graph
To run this file, make sure csv file contains 
['blocks', 'indents', 'images', 'links', 'lists', 'repo_size', 'readme_length', 'topic_score_average',
'update_interval', 'prob_popular','badge_count','language','license','time_since_last_update','Number_of_update']

Run following to get the required data:
data_retrieval_README_attr.py
data_retrieval_meta_data.py
data_retrieval_commits.py
topic_points.py
header_to_feature.py
time_based.py
"""

if __name__ == '__main__':
    __file_name = ""
    data = pd.read_csv(__file_name,
                       usecols=['name', 'user', 'readme', 'star', 'blocks', 'indents', 'images', 'links', 'lists',
                                'language',
                                'license', 'readme_length', 'topic_score_average', 'update_interval', 'prob_popular',
                                'label', 'badge_count', 'Number_of_update'])

    data['language'].fillna('None_language', inplace=True)
    data['license'].fillna('None_license', inplace=True)
    #show_label_stats(data)

    # do random forest feature importance
    language_encoder = OneHotEncoder(handle_unknown="ignore")
    license_encoder = OneHotEncoder(handle_unknown="ignore")
    numerical_pipe = Pipeline([("imputer", SimpleImputer(strategy="mean"))])
    preprocessing = ColumnTransformer(
        [
            ("language", language_encoder, ['R_ProgramLanguage']),
            ("license", license_encoder, ['R_License']),
            ("nums", numerical_pipe,
             ['R_NumCodeBlock', 'R_NumIndent', 'R_NumImage', 'R_NumLink', 'R_NumList', 'R_Length', 'P_Avg_Tag',
              'R_UpdateDensity', 'R_heading', 'R_NumBadge', 'R_NumUpdate']),
        ]
    )

    new_data = data.sample(frac=1).reset_index(drop=True)  # shuffle
    print(new_data)
    _y_train = new_data['label']
    _X_train = new_data.drop(['label'], axis=1)

    _X_train = _X_train.drop(['star', 'name', 'user', 'readme'], axis=1)
    _X_train = _X_train.rename(
        columns={"language": "R_ProgramLanguage", "license": "R_License", "blocks": "R_NumCodeBlock",
                 "indents": "R_NumIndent",
                 "images": "R_NumImage", "links": "R_NumLink", "lists": "R_NumList", "prob_popular": "R_heading",
                 "Number_of_update": "R_NumUpdate",
                 "update_interval": "R_UpdateDensity", "topic_score_average": "P_Avg_Tag", 'badge_count': 'R_NumBadge',
                 'readme_length': 'R_Length'
                 })
    print(_X_train)
    # mining.to_csv('mining.csv',index=False)
    print(len(_X_train))
    rf = Pipeline(
        [
            ("preprocess", preprocessing),
            ("classifier", RandomForestClassifier(n_estimators=200)),
        ]
    )
    X_train, X_test, y_train, y_test = train_test_split(
        _X_train, _y_train,
        test_size=0.1, random_state=42)

    cv = KFold(n_splits=10)

    score_a = cross_val_score(rf, _X_train, _y_train, cv=cv, scoring='accuracy')
    score_r = cross_val_score(rf, _X_train, _y_train, cv=cv, scoring='recall')
    score_p = cross_val_score(rf, _X_train, _y_train, cv=cv, scoring='precision')

    print("10-folds\n accuracy: %s\n recall: %s\n precision: %s\n" % (
        np.mean(score_a), np.mean(score_r), np.mean(score_p)))
    rf.fit(X_train, y_train)
    result = permutation_importance(
        rf, X_train, y_train, n_repeats=10, random_state=42, n_jobs=2, scoring='r2'
    )
    sorted_idx = result.importances_mean.argsort()
    print(len(result['importances']))
    counter = 0
    for i in list(result['importances']):
        arr = list(i)
        arr.sort()
        print(X_test.columns[counter] + " median: %f" % np.median(arr))
        counter += 1
    # regressors.stats.summary(rf['classifier'], _X_train, _y_train, X_test.columns)
    # start plot
    fig, ax = plt.subplots()
    ax.boxplot(
        result.importances[sorted_idx].T, vert=False, labels=X_test.columns[sorted_idx]
    )
    ax.set_title("Permutation Importance")
    fig.tight_layout()

    # pdp
    fig, ax = plt.subplots(figsize=(1, 1))
    ax.set_title("Random Forest PDP")
    disp = PartialDependenceDisplay.from_estimator(rf, X_test,
                                                   ['R_NumCodeBlock', 'R_NumIndent', 'R_NumImage', 'R_NumLink',
                                                    'R_NumList', 'R_Length', 'P_Avg_Tag',
                                                    'R_UpdateDensity', 'R_heading', 'R_NumBadge', 'R_NumUpdate'], ax=ax,
                                                   grid_resolution=5)
    fig.set_figwidth(15)
    fig.set_figheight(15)
    fig.tight_layout()
    plt.show()
