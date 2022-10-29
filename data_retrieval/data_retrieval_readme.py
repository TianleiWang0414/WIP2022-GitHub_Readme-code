import os

import pandas

from util.ConfigLoader import load_config
from util.connectionHelper import connector
from util.stringConstructor import buildREADMEpath
"""
To get README files, the pandaframe should have a col named user [github username]
and name [repo name]
"""
def getREADMEs(token: str, user: str, file_path: str, to_name: str) -> int:
    missing = 0
    file = os.path.abspath(file_path)
    readme = []
    readme_len = []
    data = pandas.read_csv(file)
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
                readme_len.append(len(str_response))
            ##fallback!
            except UnicodeDecodeError:
                try:
                    str_response = response.decode("cp1252")
                    print(str(index) + ":\n" + str_response)
                    readme.append(str_response)
                    readme_len.append(len(str_response))
                except UnicodeDecodeError:
                    ##nothing to do now
                    print("skipped a invalid README")
                    readme.append("Unknown encoding type")
                    readme_len.append(-1)
        else:
            missing += 1
            readme.append("Missing README or Repo no long exists")
            readme_len.append(-1)
    data['readme'] = readme
    data['readme_length'] = readme_len
    data.to_csv(to_name, index=False)
    return missing

if __name__ == '__main__':
    configs = load_config()
    __token = configs[0]
    __holder = configs[1]
    __file_name = ""
    __save_name = ""
    missing = getREADMEs(__token, __holder, __file_name, __save_name)
    print("invalid repos: %d" % (missing))