import json

from util.ConfigLoader import load_config
from util.stringConstructor import buildContributorsPath, buildWatches, buildPulllRequests, buildRepoStatusPath
from util.connectionHelper import connector
import re
import pandas

pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)

"""
This file is able to get repo basic infos (see get_stats(token:str,user:str))
The pandaframe should have a col named user [github username]
and name [repo name]
"""
def api_call_handler(conn, frame: list, defalut: int):
    try:
        conn.getResponse()
        header = conn.headerResponse
        str_response = header.decode("utf-8")
        last_page = get_count(str_response)
        frame.append(last_page)
        print(re.findall('x-ratelimit-remaining:.+', str_response))
    except:
        frame.append(defalut)


def get_count(string: str) -> int:
    link = re.findall('link:.+', string)

    link_last_part = link[0].split(',')[1]
    page = link_last_part.split(';')[0].split('?')[1]
    last_page = int(page.split('&')[-1].split('=')[1].replace('>', ''))
    # print(last_page)
    return last_page


def get_stats(token: str, user: str, file_name: str, to_name: str):
    data = pandas.read_csv(file_name)
    data = data.drop_duplicates()
    contributor_number = []
    watches_number = []
    pull_requests = []
    stars = []
    forks = []
    counter = 0
    ##max = 600
    for index, row in data.iterrows():
        if counter == max:
            break
        print(counter)
        counter += 1
        org = row['user']
        repo = row['name']
        print('%s/%s' % (org, repo))
        # contributor
        url = buildContributorsPath(org, repo)
        conn = connector(url, token, user)
        api_call_handler(conn, contributor_number, 1)
        # watches
        url = buildWatches(org, repo)
        conn = connector(url, token, user)
        api_call_handler(conn, watches_number, 1)
        # num of pull requests
        url = buildPulllRequests(org, repo)
        conn = connector(url, token, user)
        api_call_handler(conn, pull_requests, 0)
        # stars and forks
        url = buildRepoStatusPath(org, repo)
        conn = connector(url, token, user)
        response = conn.getResponse()
        print(response)

        if conn.response_code == 200:
            decoding = json.loads(response)
            stars_c = decoding['watchers_count']
            forks_c = decoding['forks_count']

            stars.append(stars_c)
            forks.append(forks_c)

        elif conn.response_code == 300:
            decoding = json.loads(response)
            location = decoding['url']
            redirect = connector(location, token, user)
            new_response = redirect.getResponse()
            decoding = json.loads(new_response)
            stars_c = decoding['watchers_count']
            forks_c = decoding['forks_count']

            stars.append(stars_c)
            forks.append(forks_c)
        else:
            stars.append(0)
            forks.append(0)
    while counter < len(data):
        contributor_number.append([None])
        watches_number.append(None)
        pull_requests.append(None)
        stars.append(None)
        forks.append(None)
        counter += 1
    data['contributors'] = contributor_number
    data['star'] = stars
    data['watch'] = watches_number
    data['pull_requests'] = pull_requests
    data['fork'] = forks

    print(len(data))
    data.to_csv(to_name, index=False)


if __name__ == '__main__':
    configs = load_config()
    __token = configs[0]
    __holder = configs[1]
    ##Change the file name here
    __file_name = ""
    __save_name = ""
    get_stats(__token, __holder, __file_name, __save_name)
