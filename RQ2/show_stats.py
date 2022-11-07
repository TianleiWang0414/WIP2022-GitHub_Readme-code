"""
This file generates stats for popular and non-popular groups

Run following to get the required data:
data_retrieval_README_attr.py
data_retrieval_meta_data.py
data_retrieval_commits.py
topic_points.py
header_to_feature.py
time_based.py
"""
import pandas
import pandas as pd
from matplotlib import pyplot as plt

from RQ2.RQ2_util.split_popular import get_non_popular, get_popular


def __print_stats(frame: pd.DataFrame):
    col = ['watch', 'fork', 'star', 'repo_size', 'repo_created']
    for i in col:
        mean = frame[i].mean()
        median = frame[i].median()
        col_min = frame[i].min()
        col_max = frame[i].max()
        print("%s:  mean -> %f median->%s min->%f max->%f" % (
            i, mean, median,
            col_min, col_max))


def show_label_stats(data: pd.DataFrame):
    top_stats = get_popular(data)
    bottom_stats = get_non_popular(data)

    print("Top_stats:")
    __print_stats(top_stats)
    print("\nBottom_stats")
    __print_stats(bottom_stats)


def star_distribution(data: pd.DataFrame):
    bin_name = ['[0 , 100]',
                '(100 , 1000]',
                '(1000 , 5000]',
                '(5000 , 20000]',
                '(20000 , inf)',
                ]
    percentage = [0] * len(bin_name)
    for _, row in data.iterrows():
        star = row['star']
        if star <= 100:
            percentage[0] += 1
        elif 100 < star <= 1000:
            percentage[1] += 1
        elif 1000 < star <= 5000:
            percentage[2] += 1
        elif 5000 < star <= 20000:
            percentage[3] += 1
        elif star > 20000:
            percentage[4] += 1
    print("bin stats: ")
    print(percentage)
    width = 0.3
    plt.bar(bin_name, height=percentage, width=width)

    title = "Star distribution"
    plt.xlabel("stars")
    plt.ylabel("frequency")
    plt.title(title)

    plt.show()


if __name__ == "__main__":
    __file_name = ""
    data = pandas.read_csv(__file_name)
    show_label_stats(data)
    star_distribution(data)
