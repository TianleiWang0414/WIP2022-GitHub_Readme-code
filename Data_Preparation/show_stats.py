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
from IPython.display import display

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, 'D:/paper/WIP2022-GitHub_Readme-code/')
from  RQ2.RQ2_util.split_popular  import get_non_popular, get_popular, load_data


def __print_stats(frame: pd.DataFrame):
    print(len(frame))
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

def show_Top_50_star(data: pd.DataFrame):
    df =  data.sort_values(by='star',ascending=False)
    display(df)
     


def star_distribution(data: pd.DataFrame):
    bin_name = ['[0]',
                '[0 , 100]',
                '(100 , 1000]',
                '(1000 , 5000]',
                '(5000 , 20000]',
                '(20000 , inf)',
                ]
    percentage = [0] * len(bin_name)
    for _, row in data.iterrows():
        star = row['star']
        if star == 0:
            percentage[0] += 1
        elif 0 < star <= 100:
            percentage[1] += 1
        elif 100 < star <= 1000:
            percentage[2] += 1
        elif 1000 < star <= 5000:
            percentage[3] += 1
        elif 5000 < star <= 20000:
            percentage[4] += 1
        elif star > 20000:
            percentage[5] += 1
    print("bin stats: ")
    print(percentage)
    width = 0.3
   
    plt.bar(bin_name, height=percentage, width=width)

    title = "Star distribution"
    plt.xlabel("stars")
    plt.ylabel("frequency")
    plt.title(title)

    plt.show()


#def getBasicInfo(data: pd.DataFrame):



#if __name__ == "__main__":

data = load_data("D:/paper/WIP2022-GitHub_Readme-code/data/all_in_one_data.csv")
#show_label_stats(data)
star_distribution(data)
plt.hist(data['star'])

title = "Star distribution"
plt.xlabel("stars")
plt.ylabel("frequency")
plt.title(title)
plt.show()
show_Top_50_star(data)

