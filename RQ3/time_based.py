import numpy
import numpy as np
import json
import ast
import pandas
from datetime import date
from util.ConfigLoader import load_config

import matplotlib.pyplot as plt

"""
This file parse raw commits into average_update, Number_of_update, message(commit message)
, time_since_last_update, and update_interval. 
The file also create a distribution graph for average update

Run following to get the required data:
data_retrieval_meta_data.py
data_retrieval_commits.py
"""


def print_observation(file_name: str, to_name: str):
    data = pandas.read_csv(file_name)
    num_row = len(data)
    total_commits = 0
    total_commits_noDup = 0
    total_diff_time = 0.
    total_no_commit = 0
    max_commit = 0
    min_commit = 9999
    max_day = 0
    min_day = 9999
    # the Format we store is a list of lists. Each list in this list is a repo, and within is the messages(commit
    # happened in same day are grouped)
    all_message = []
    commit_length = []
    days = []
    for index, row in data.iterrows():

        commits = row['commits']
        commits_list = ast.literal_eval(commits)
        pre = None
        commit_list = []
        repo_list = []
        message_same_day = []

        for commit in commits_list:
            # Get Year,month, and day
            time = commit['commit']['committer']['date'].split("T")[0].split("-")

            year = int(time[0])
            month = int(time[1].lstrip('0'))
            day = int(time[2].lstrip('0'))
            curr = date(year, month, day)

            # update on the same day? group them
            if curr == pre:
                if len(message_same_day) == 0:
                    last = repo_list[-1]
                    message_same_day.append(last)
                message_same_day.append(commit['commit']['message'])
            else:
                if len(message_same_day) > 0:
                    repo_list.pop()
                    repo_list.append(message_same_day)
                    message_same_day = []
                repo_list.append(commit['commit']['message'])
                commit_list.append(curr)

            pre = curr
        commit_length.append(len(repo_list))
        all_message.append(repo_list)
        commit_list = sorted(commit_list)
        current_delta = 0
        if len(commit_list) > 0:
            first = commit_list[0]
            for index in range(1, len(commit_list)):
                second = commit_list[index]
                delta = second - first
                total_diff_time += delta.days
                current_delta += delta.days
                max_day = max(delta.days, max_day)
                min_day = min(delta.days, min_day)
                first = second

            total_commits_noDup += len(commit_list)
            current_delta /= len(commit_list)
            days.append(current_delta)
        else:
            days.append(-1)
        length = len(commits_list)
        total_commits += length
        max_commit = max(max_commit, length)
        min_commit = min(min_commit, length)
        if length == 0:
            total_no_commit += 1
    # This checks if we missed any grouping
    # check = 0
    # for i in all_message:
    #     check+=len(i)
    # print(check)

    # print out averages
    print("Total commits: %d" % total_commits)
    print("Total commits after grouping: %d" % total_commits_noDup)
    print("Average number of commits per README: %d\n max: %d and min: %d" % (
        total_commits / num_row, max_commit, min_commit))
    print("Average days of updating the README: %f\n max: %d and min: %d" % (
        total_diff_time / total_commits, max_day, min_day))
    print("Average days of updating the README(without multi update on the same day): %f" % (
            total_diff_time / total_commits_noDup))
    print("Number of repos never changed README： %d" % total_no_commit)
    # These two json file is needed for other features
    with open('time.json', 'w') as f:
        json.dump(days, f)

    with open('message.json', 'w') as f:
        json.dump(all_message, f)

    data['message'] = all_message
    data['average_update'] = days
    data['Number_of_update'] = commit_length
    data.to_csv(to_name, index=False)


# Return age_data for plot
def get_update_interval(file_name: str, to_name: str) -> list:
    data = pandas.read_csv(file_name)

    data['repo_created'].fillna('%s-%s-%sT' % (1970, 1, 1), inplace=True)
    time_date = data['repo_created']
    freq = data['Number_of_update']
    age_data = []

    for date_created in time_date:
        parse_date = str(date_created).split("T")[0].split("-")
        created = date(int(parse_date[0]), int(parse_date[1].lstrip('0')), int(parse_date[2].lstrip('0')))
        age = today - created
        age_data.append(age.days)

    counter = 0
    for num_updates in freq:
        res = float(age_data[counter]) / (num_updates + 1)
        # print(res)
        if not numpy.isnan(float(res)):
            res = round(res)
        else:
            old = date(1970, 1, 1)

            res = (today - old).days
        age_data[counter] = res
        counter += 1
    time = age_data
    # update_interval = total_days/update_freq
    data['update_interval'] = time
    data.to_csv(to_name, index=False)
    return age_data


def get_time_since_last_update(file_name: str, to_name: str):
    data = pandas.read_csv(file_name)
    time_since_last_update = []
    for index, row in data.iterrows():

        commits = ast.literal_eval(row['commits'])
        latest = date(1970, 1, 1)
        # if it is never updated, then it is the same as when it is created
        if len(commits) == 0:
            time_since_last_update.append(row['repo_created'])
            continue
        # print(commits)
        for commit in commits:
            time = commit['commit']['committer']['date'].split("T")[0].split("-")
            year = int(time[0])
            month = int(time[1].lstrip('0'))
            day = int(time[2].lstrip('0'))
            curr = date(year, month, day)

            if curr > latest:
                latest = curr

        delta = today - latest
        # print(latest)
        time_since_last_update.append(delta.days)
        # print(time_since_last_update)
    data['time_since_last_update'] = time_since_last_update
    data.to_csv(to_name, index=False)


# distribution graph for average update
def plot_average_update_graph(age_data: list):
    bin_name = ['< 1 day',
                '1 day -> 1 week',
                '1 week -> 1 month',
                '1 month-> 6 month',
                '6 month -> 1 year',
                '1 year -> inf'
                ]
    # Plot the PDF.
    percentage = [0, 0, 0, 0, 0, 0]
    sort = np.sort(age_data)
    print(len(sort))
    for i in sort:
        if i <= 1:
            percentage[0] += 1
        elif 1 < i <= 7:
            percentage[1] += 1
        elif 7 < i <= 31:
            percentage[2] += 1
        elif 31 < i <= 183:
            percentage[3] += 1
        elif 183 < i <= 365:
            percentage[4] += 1
        else:
            percentage[5] += 1
    y_axis = [y / len(sort) for y in percentage]
    print(percentage)
    width = 0.3
    fig, axes = plt.subplots(figsize=(7, 5), dpi=100)
    plt.bar(bin_name, height=percentage, width=width)
    axes.set_xticklabels(bin_name, rotation=45, rotation_mode="anchor", ha="right")

    title = "Distribution Of Updating Time"
    plt.xlabel("update time (days/update_freq)")
    plt.ylabel("percentage")
    plt.title(title)

    plt.show()


if __name__ == "__main__":
    configs = load_config()
    today = date.today()
    __file_name = ""
    __save_name = ""
    # get features
    print_observation(__file_name, __save_name)
    age_data = get_update_interval(__save_name, __save_name)
    get_time_since_last_update(__save_name, __save_name)

    # Plot the histogram.
    plot_average_update_graph(age_data)
