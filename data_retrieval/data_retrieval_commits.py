import json
import os
import pandas

from util.ConfigLoader import load_config
from util.stringConstructor import buildREADMECommitPath
from util.connectionHelper import connector

"""
This file retrieves README commits from GitHub 
input csv file is required to have a col named user [github username]
and name [repo name]
"""


def getCommit(token: str, user: str, file_name: str, to_name: str):
    # check the data difference and added commit to those new data
    file = os.path.abspath(file_name)  # path
    commits = []
    data = pandas.read_csv(file)
    for index, row in data.iterrows():
        org = row['user']
        repo_name = row['name']

        # check master and main branch
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
    data['commits'] = commits

    data.to_csv(to_name, index=False)
    return


if __name__ == "__main__":
    configs = load_config()
    __file_name = ""
    __save_name = ""
    getCommit(configs[0], configs[1], __file_name, __save_name)
