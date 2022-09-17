import os

import pandas

from RQ1.prune_related.prunning import valid
from util.ConfigLoader import load_config
from util.connectionHelper import connector
from util.stringConstructor import buildREADMEpath

"""
this function creates a new file that contains readme
returns how many repos does not have README
"""


def getREADMEs(token: str, user: str) -> int:
    missing = 0
    col = ["name", "user"]
    file = os.path.abspath("../data/Github_data.csv")
    readme = []

    data = pandas.read_csv(file, usecols=col)
    for index, row in data.iterrows():
        org = row['user']
        repo_name = row['name']
        url = buildREADMEpath(org, repo_name)
        conn = connector(url, token, user)
        response = conn.getResponse()
        if response is not None:
            try:
                str_response = response.decode("utf-8")
                print(str(index) + ":\n" + str_response)
                readme.append(str_response)
            ##fallback!
            except UnicodeDecodeError:
                try:
                    str_response = response.decode("cp1252")
                    print(str(index) + ":\n" + str_response)
                    readme.append(str_response)
                except UnicodeDecodeError:
                    ##nothing to do now
                    print("skipped a invalid README")
                    readme.append("Unknown encoding type")

        else:
            missing += 1
            readme.append("Missing README or Repo no long exists")
    data['readme'] = readme
    data.to_csv("dataWithREADME.csv")
    return missing


if __name__ == '__main__':
    # load config
    configs = load_config()
    __token = configs[0]
    __holder = configs[1]
    ## speed up a bit if we have the data
    if not os.path.isfile('./dataWithREADME.csv'):
        missing = getREADMEs(__token, __holder)
        print("invalid repos: %d" %(missing))
    invalid_length = 0
    invalid_language = 0
    invalid_heading = 0
    if not os.path.isfile('../data/cleaned_data.csv'):
        data = pandas.read_csv("./dataWithREADME.csv")
        data = data.dropna()
        for index, row in data.iterrows():
            readme = row['readme']
            validation=valid(readme,row['name'])
            if not validation[0]:
                data.drop(index, inplace=True)
                reason= validation[1]
                if reason==0 :
                    invalid_length+=1
                elif reason==1:
                    invalid_language+=1
                elif reason==2:
                    invalid_heading+=1
        data=data.drop_duplicates(subset=['name','user'])
        print("Pruned:")
        print("Default README: %d" %(invalid_length))
        print("README not in English: %d" % (invalid_language))
        print("README with no heading: %d" % (invalid_heading))
        data.to_csv("cleaned_data.csv",index=False)
    data_file = pandas.read_csv('../data/cleaned_data.csv')

    #file = file.drop(, inplace=True)
    invalid = data_file[data_file['readme'] == 'Missing README or Repo no long exists'].index
    data_file.drop(invalid, inplace=True)
    data_file.drop_duplicates()
    print(len(data_file))
    data_file.to_csv('../data/cleaned_data.csv',index=False)
    print("complete")
