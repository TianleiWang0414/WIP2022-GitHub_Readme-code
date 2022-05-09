from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance, PartialDependenceDisplay
from pdpbox import pdp, get_dataset, info_plots
from sklearn.model_selection import train_test_split, cross_val_score, KFold, cross_validate
from scipy import stats
import statsmodels.api as sm
from sklearn.preprocessing import LabelBinarizer, OneHotEncoder
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn.impute import SimpleImputer
from datetime import date
import regressors.stats
import pandas as pd

if __name__ == '__main__':
    data = pd.read_csv('rf_data(new).csv',
                       usecols=['name','user','readme','star', 'blocks', 'indents', 'images', 'links', 'lists', 'language',
                                'license','readme_length','topic_score_average' ,'update_interval', 'prob_popular','label','badge_count', 'Number_of_update'])
    stats_data = pd.read_csv('rank_repo.csv',
                              usecols=['contributors', 'star', 'fork', 'watch', 'pull_requests', 'rank_point'])

    data['language'].fillna('None_language', inplace=True)
    data['license'].fillna('None_license', inplace=True)
    print(len(data))
    language_encoder =  OneHotEncoder(handle_unknown="ignore")
    license_encoder =  OneHotEncoder(handle_unknown="ignore")
    numerical_pipe = Pipeline([("imputer", SimpleImputer(strategy="mean"))])
    preprocessing = ColumnTransformer(
        [
            ("language", language_encoder, ['R_ProgramLanguage']),
            ("license", license_encoder, ['R_License']),
            ("nums", numerical_pipe,
             ['R_NumCodeBlock', 'R_NumIndent', 'R_NumImage', 'R_NumLink', 'R_NumList', 'R_Length', 'P_Avg_Tag',
              'R_UpdateDensity', 'R_heading','R_NumBadge','R_NumUpdate']),
        ]
    )

#    data = data[data['repo_size'].notna()]
    length = int(len(data) * 0.2)


    top_stats = stats_data.nlargest(n=length, columns=['star'])
    bottom_stats = stats_data.nsmallest(n=length, columns=['star'])

    print("watch:  mean -> %f median->%s min->%f max->%f" % (
        top_stats['watch'].mean(), top_stats['watch'].median(),
        top_stats['watch'].min(),
        top_stats['watch'].max()))
    print("fork:  mean -> %f median->%s min->%f max->%f" % (
        top_stats['fork'].mean(), top_stats['fork'].median(),
        top_stats['fork'].min(),
        top_stats['fork'].max()))

    print("watch:  mean -> %f median->%s min->%f max->%f" % (
        bottom_stats['watch'].mean(), bottom_stats['watch'].median(),
        bottom_stats['watch'].min(),
        bottom_stats['watch'].max()))
    print("fork:  mean -> %f median->%s min->%f max->%f" % (
        bottom_stats['fork'].mean(), bottom_stats['fork'].median(),
        bottom_stats['fork'].min(),
        bottom_stats['fork'].max()))
    # mining = new_data
    # mining.to_csv('mining.csv', index=False)
    new_data = data.sample(frac=1).reset_index(drop=True)  # shuffle
    print(new_data)
    _y_train = new_data['label']
    _X_train = new_data.drop(['label'], axis=1)

    _X_train = _X_train.drop(['star','name','user','readme'], axis=1)
    _X_train = _X_train.rename(
        columns={"language": "R_ProgramLanguage", "license": "R_License", "blocks": "R_NumCodeBlock",
                 "indents": "R_NumIndent",
                 "images": "R_NumImage", "links": "R_NumLink", "lists": "R_NumList", "prob_popular": "R_heading",
                 "Number_of_update": "R_NumUpdate",
                 "update_interval": "R_UpdateDensity", "topic_score_average": "P_Avg_Tag", 'badge_count': 'R_NumBadge',
                 'readme_length': 'R_Length'
                 })
    print(_X_train)
    #mining.to_csv('mining.csv',index=False)
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
        rf,X_train , y_train, n_repeats=10, random_state=42, n_jobs=2,scoring='r2'
    )
    sorted_idx = result.importances_mean.argsort()
    print(len(result['importances']))
    counter = 0
    for i in list(result['importances']):
        arr = list(i)
        arr.sort()
        print(X_test.columns[counter] + " median: %f" % np.median(arr))
        counter+=1
    #regressors.stats.summary(rf['classifier'], _X_train, _y_train, X_test.columns)
    fig, ax = plt.subplots()
    ax.boxplot(
        result.importances[sorted_idx].T, vert=False, labels=X_test.columns[sorted_idx]
    )
    ax.set_title("Permutation Importance")
    fig.tight_layout()




    #pdp
    fig, ax = plt.subplots(figsize=(1, 1))
    ax.set_title("Random Forest PDP")
    disp = PartialDependenceDisplay.from_estimator(rf, X_test, ['R_NumCodeBlock', 'R_NumIndent', 'R_NumImage', 'R_NumLink', 'R_NumList', 'R_Length', 'P_Avg_Tag',
              'R_UpdateDensity', 'R_heading','R_NumBadge','R_NumUpdate'],ax=ax,grid_resolution=5)
    fig.set_figwidth(15)
    fig.set_figheight(15)
    fig.tight_layout()
    plt.show()







