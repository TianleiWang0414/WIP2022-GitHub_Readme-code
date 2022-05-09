import json
import re

from util.ConfigLoader import load_config
from util.connectionHelper import connector
from util.stringConstructor import buildRepoStatusPath
import pandas

if __name__ == '__main__':
    info = pandas.read_csv('popularity_repo.csv')

    language = []
    repo_size = []
    repo_created = []
    license = []
    topics = []
    token ,user = load_config()

    #max = 10
    for index,row in info.iterrows():
        if index == max:
            break
        org = row['user']
        repo = row['name']
        url = buildRepoStatusPath(org, repo)
        conn = connector(url, token, user)
        response = conn.getResponse()
        print(response)
        if conn.response_code == 200:
            decoding = json.loads(response)
            curr_lang = decoding['language']
            curr_create = decoding['created_at']
            curr_size = decoding['size']
            curr_license = decoding['license']
            curr_topics= decoding['topics']
            if curr_license:
                license.append(curr_license['key'])
            else:
                license.append(None)
            language.append(curr_lang)
            repo_size.append(curr_size)
            repo_created.append(curr_create)
            topics.append(curr_topics)
        elif conn.response_code == 300:
            decoding = json.loads(response)
            location = decoding['url']
            redirect = connector(location, token, user)
            new_response = redirect.getResponse()

            decoding = json.loads(new_response)
            curr_lang = decoding['language']
            curr_create = decoding['created_at']
            curr_size = decoding['size']
            curr_license = decoding['license']
            curr_topics = decoding['topics']
            if curr_license:
                license.append(curr_license['key'])
            else:
                license.append(None)
            language.append(curr_lang)
            repo_size.append(curr_size)
            repo_created.append(curr_create)
            topics.append(curr_topics)
        else:
            print("%s/%s failed"%(org,repo))
            language.append(None)
            repo_size.append(None)
            repo_created.append(None)
            license.append(None)
            topics.append(None)

    info['language'] = language
    info['repo_size'] = repo_size
    info['repo_created'] = repo_created
    info['license'] = license
    info['topics'] = topics

    info.to_csv('popularity_repo.csv', index = False)