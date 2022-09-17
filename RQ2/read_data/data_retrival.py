import json
import os

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
"""
def api_call_handler(conn,frame:list,defalut:int):
    try:
        conn.getResponse()
        header = conn.headerResponse
        str_response = header.decode("utf-8")
        last_page = get_count(str_response)
        frame.append(last_page)
        print(re.findall('x-ratelimit-remaining:.+',str_response))
    except:
        frame.append(defalut)
def get_count(string:str) -> int:
    link = re.findall('link:.+', string)

    link_last_part = link[0].split(',')[1]
    page = link_last_part.split(';')[0].split('?')[1]
    last_page = int(page.split('&')[-1].split('=')[1].replace('>', ''))
    #print(last_page)
    return last_page

def get_stats(token:str,user:str):
    data= pandas.read_csv('../data/cleaned_data.csv',usecols=['name','user','readme'])
    old_data = pandas.read_csv('popularity_repo.csv')
    print(len(old_data))
    print(len(data))
    df_all = data.merge(old_data.drop_duplicates(), on=['name', 'user'],
                       how='left', indicator=True)
    df_diff = df_all[df_all['_merge'] == 'left_only'].drop(columns=['readme_y','_merge'])
    df_diff = df_diff.rename(columns={"readme_x":"readme"})
    print("%d left\n"%len(df_diff) )
    contributor_number= []
    watches_number = []
    pull_requests = []
    stars = []
    forks = []
    counter = 0
    ##max = 600
    for index,row in df_diff.iterrows():
        if counter == max:
            break
        print(counter)
        counter += 1
        org = row['user']
        repo = row['name']
        print ('%s/%s' % (org,repo))
        #contributor
        url = buildContributorsPath(org,repo)
        conn = connector(url,token,user)
        api_call_handler(conn,contributor_number,1)
        #watches
        url = buildWatches(org,repo)
        conn = connector(url, token, user)
        api_call_handler(conn, watches_number, 1)
        #num of pull requests
        url = buildPulllRequests(org,repo)
        conn = connector(url, token, user)
        api_call_handler(conn, pull_requests, 0)
        #stars and forks
        url = buildRepoStatusPath(org,repo)
        conn =connector(url, token, user)
        response = conn.getResponse()
        print(response)
        #print(url)
        if conn.response_code == 200:
            decoding = json.loads(response)
            stars_c = decoding['watchers_count']
            forks_c = decoding['forks_count']

            stars.append(stars_c)
            forks.append(forks_c)

            #print(stars_c)
            #print(forks_c)
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
    while counter < len(df_diff):
        contributor_number.append([None])
        watches_number.append(None)
        pull_requests.append(None)
        stars.append(None)
        forks.append(None)
        counter += 1
    df_diff['contributors'] = contributor_number
    df_diff['star'] = stars
    df_diff['watch'] = watches_number
    df_diff['pull_requests'] = pull_requests
    df_diff['fork'] = forks
    new_data = old_data.append(df_diff,ignore_index=True)

    new_data = new_data.drop_duplicates()
    print(len(new_data))
    new_data.to_csv('popularity_repo.csv',index=False)




if __name__ == '__main__':
    configs = load_config()
    __token = configs[0]
    __holder = configs[1]
    get_stats(__token,__holder)




