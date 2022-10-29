from datetime import date
import numpy
import pandas
import ast

"""
This file is able to find the duration (in days) of the repo since last update.
"""
if __name__ == "__main__":

    data= pandas.read_csv("commitsData1.csv",usecols=['name','user','commits','message','length'])
    print(numpy.sum(data['length']))
    data_choose = pandas.read_csv("../RQ3/rf_data(new).csv")


    popular = data_choose.loc[data_choose['label'] != 0]

    non_popular = data_choose.loc[data_choose['label'] == 0]
    print(len(non_popular))

    df_all = popular.merge(data.drop_duplicates(), on=['name', 'user'],
                        how='inner', indicator=True)
    df_all = df_all.drop(columns=['_merge'])
    print(df_all.loc[df_all['badge_count']>0])
    today= date.today() #2022/04/30

    time_since_last_update = []
    print(df_all)
    for index,row in df_all.iterrows():

        commits= ast.literal_eval(row['commits'])
        latest = date(1970, 1, 1)
        #print(len(commits))
        if len(commits) ==0:
            time_since_last_update.append(row['repo_created'])
            continue
        #print(commits)
        for commit in commits:
            time = commit['commit']['committer']['date'].split("T")[0].split("-")
            year = int(time[0])
            month = int(time[1].lstrip('0'))
            day = int(time[2].lstrip('0'))
            curr = date(year, month, day)

            if curr> latest:
                latest= curr

        delta = today - latest
        #print(latest)
        time_since_last_update.append(delta.days)
        #print(time_since_last_update)
    data_choose['time_since_last_update'] = time_since_last_update
    data_choose.to_csv("rf_data(new).csv",index=False)
