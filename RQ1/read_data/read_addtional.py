import pandas
import json

"""
Used add more repos to our dataset.
real data retrieval is in RQ2
"""
from util.connectionHelper import connector
from util.stringConstructor import buildREADMEpath
from util.ConfigLoader import load_config
if __name__ == "__main__":
    # configs = load_config()
    # __token = configs[0]
    # __holder = configs[1]
    # file =open('../data/additional_repo.json')
    # repo_list=json.load(file)
    # print(len(repo_list))
    # start = 4000
    # end = 5000
    # name= []
    # user =[]
    # readme = []
    # for index in range(start,end):
    #     info = repo_list[index]['repo_name'].split('/')
    #     owner = info[0]
    #     repo = info[1]
    #     url = buildREADMEpath(owner, repo)
    #     conn = connector(url,__token,__holder)
    #     response = conn.getResponse()
    #     if response is not None:
    #         try:
    #             str_response = response.decode("utf-8")
    #             print(str(index) + ":\n" + str_response)
    #             readme.append(str_response)
    #             name.append(repo)
    #             user.append(owner)
    #
    #         ##fallback!
    #         except UnicodeDecodeError:
    #             try:
    #                 str_response = response.decode("cp1252")
    #                 print(str(index) + ":\n" + str_response)
    #                 readme.append(str_response)
    #                 name.append(repo)
    #                 user.append(owner)
    #             except UnicodeDecodeError:
    #                 ##nothing to do now
    #                 print("skipped a invalid README")
    #                 readme.append("Unknown encoding type")
    #                 name.append(repo)
    #                 user.append(owner)
    #
    # d = {'name':name,'user':user,'readme':readme}
    # frame = pandas.read_csv('additional_DataWithReadme.csv')
    # new_data= pandas.DataFrame(data=d)
    # frame=frame.append(new_data,ignore_index=True)
    # frame.to_csv('additional_DataWithReadme.csv',index=False)

    data = pandas.read_csv('dataWithREADME.csv', usecols = ['name' , 'user' , 'readme'])
    print(data)