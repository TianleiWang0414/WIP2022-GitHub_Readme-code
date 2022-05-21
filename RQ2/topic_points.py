import pandas
import json
import time
import numpy
from util.ConfigLoader import load_config
from util.connectionHelper import connector
from util.stringConstructor import buildTopicSearch
from ast import literal_eval
def topic_json(token, user):
    topic_dict = {}
    data = pandas.read_csv("popularity_repo.csv")

    data['topics'].fillna('[]',inplace=True)
    data.topics = data.topics.apply(literal_eval)
    for _,row in data.iterrows():
        topics = row['topics']
        if not topics:
            continue

        print(topics)
        for topic in topics:

            if topic not in topic_dict:
                topic_link = buildTopicSearch(topic)
                conn = connector(topic_link, token, user)
                response  = conn.getResponse()
                if conn.response_code == 200:
                    decoding = json.loads(response)
                    count = decoding['total_count']
                    topic_dict[topic] = count
                    print(len(topic_dict))
                    print(topic_dict)
                    time.sleep(2)

    with open('topic.json', 'w') as f:
            json.dump(topic_dict, f)


if __name__ == "__main__":
    configs = load_config()
    __token = configs[0]
    __holder = configs[1]
    #topic_json(__token, __holder)
    lrm_data = pandas.read_csv('RQ3 ReadmeStatsByRanking.csv')
    cross_ref = pandas.read_csv('popularity_repo.csv')
    cross_ref['topics'].fillna('[]', inplace=True)
    cross_ref.topics = cross_ref.topics.apply(literal_eval)
    topic_score_sum = []
    topic_score_average = []
    topic_score_median = []
    topic_score_max= []
    with open('topic.json', 'r') as f:
        topics = json.load(f)
    for _,row in lrm_data.iterrows():
        cross_row = cross_ref.loc[(cross_ref['name']==row['name']) & (cross_ref['user']==row['user'])]
        for x in cross_row['topics']:
            curr_score = []
            for topic in x:
                curr_score.append(topics[topic])
            print(curr_score)
            if len(curr_score) >0:
                topic_score_max.append(numpy.max(curr_score))
                topic_score_sum.append(numpy.sum(curr_score))
                topic_score_average.append(numpy.mean(curr_score))
                topic_score_median.append(numpy.median(curr_score))
            else:
                topic_score_max.append(0)
                topic_score_sum.append(0)
                topic_score_average.append(0)
                topic_score_median.append(0)

    lrm_data['topic_score_sum'] = topic_score_sum
    lrm_data['topic_score_average'] = topic_score_average
    lrm_data['topic_score_median'] = topic_score_median
    lrm_data['topic_score_max'] = topic_score_max

    lrm_data.to_csv('RQ3 ReadmeStatsByRanking.csv',index = False)





