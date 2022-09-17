import numpy as np
import json
import os
import ast
import pandas
from datetime import date

from RQ2.time_based import print_observation
from util.ConfigLoader import load_config
from util.stringConstructor import buildREADMECommitPath
from util.connectionHelper import connector

"""This method retrieves README commits from GitHub """


def getCommit(token: str, user: str):
    col = ["name", "user"]

    #check the data difference and added commit to those new data
    file = os.path.abspath("../RQ1/cleaned_data.csv") #path
    done = pandas.read_csv('commitsData.csv')
    commits = []
    name = []
    _user = []
    data = pandas.read_csv(file, usecols=col)
    possible_missed = done[done['commits'] == "[]"]
    print(possible_missed)
    for index, row in data.iterrows():
        print(index)
        org = row['user']
        repo_name = row['name']
        # got entry for it
        found = possible_missed.loc[(possible_missed['name'] == repo_name) & (possible_missed['user'] == org)]
        if len(found) == 0:
            continue
        print(org + " " + repo_name)
        _user.append(org)
        name.append(repo_name)
        url = buildREADMECommitPath(org, repo_name, 'master')
        conn = connector(url, token, user)
        response = conn.getResponse()
        if response is not None:
            decoding = json.loads(response)
            commits.append(decoding)
        else:
            url = buildREADMECommitPath(org, repo_name, 'main')
            conn = connector(url, token, user)
            response = conn.getResponse()
            if response is not None:
                decoding = json.loads(response)
                commits.append(decoding)
            else:
                commits.append([])
    new_data = {'name': name,'user':_user,'commits':commits}
    df = pandas.DataFrame(data=new_data)
    done.append(df)
    done.drop_duplicates(subset=['name', 'user'],keep='last')
    done.to_csv("commitsData.csv", index=False)
    return





if __name__ == "__main__":
    configs = load_config()
    getCommit(configs[0], configs[1])
    print_observation()
