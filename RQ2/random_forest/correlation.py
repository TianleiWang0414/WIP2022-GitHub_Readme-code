import numpy as np
import pandas as pd
import seaborn as sns  # For pairplots and heatmaps
import matplotlib.pyplot as plt

"""
Spearman correlation
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


# https://stackabuse.com/calculating-spearmans-rank-correlation-coefficient-in-python-with-pandas/
def display_correlation(df):
    r = df.corr(method="spearman")
    plt.figure(figsize=(20, 20))
    heatmap = sns.heatmap(df.corr(), vmin=-1,
                          vmax=1, annot=True)
    plt.title("Spearman Correlation")
    plt.show()


if __name__ == '__main__':
    __file_name = ""
    # ADD new metrics here
    file = pd.read_csv(__file_name,
                       usecols=['star','blocks', 'indents', 'images', 'links', 'lists', 'repo_size', 'readme_length',
                                'topic_score_average',
                                'update_interval', 'prob_popular', 'badge_count', 'language', 'license',
                                'time_since_last_update', 'Number_of_update'])

    transform = file.apply(lambda x: pd.factorize(x)[0])
    correlation = transform.corr(method='spearman')
    display_correlation(transform)
    print(correlation)
