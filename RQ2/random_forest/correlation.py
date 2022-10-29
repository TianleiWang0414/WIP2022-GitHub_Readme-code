import numpy as np
import pandas as pd
import seaborn as sns # For pairplots and heatmaps
import matplotlib.pyplot as plt
"""
Spearman correlation
To run this file, make sure csv file contains 
['blocks', 'indents', 'images', 'links', 'lists', 'repo_size', 'readme_length', 'topic_score_average',
'update_interval', 'prob_popular','badge_count','language','license','time_since_last_update','Number_of_update']

Run following to get the data:
data_retrieval_README_attr.py
data_retrieval_meta_data.py
topic_points.py
header_to_feature.py
"""
def display_correlation(df):
    r = df.corr(method="spearman")
    plt.figure(figsize=(10,10))
    heatmap = sns.heatmap(df.corr(), vmin=-1,
                      vmax=1, annot=True)
    plt.title("Spearman Correlation")
    plt.show()
if __name__ == '__main__':
    file = pd.read_csv("rf_data(new).csv", usecols=['blocks', 'indents', 'images', 'links', 'lists', 'repo_size', 'readme_length', 'topic_score_average',
              'update_interval', 'prob_popular','badge_count','language','license','time_since_last_update','Number_of_update'])

    transform = file.apply(lambda x : pd.factorize(x)[0])
    correlation = transform.corr(method='spearman')
    display_correlation(transform)
    print(correlation)