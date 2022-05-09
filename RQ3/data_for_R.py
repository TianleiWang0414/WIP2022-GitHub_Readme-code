import pandas


if __name__ == "__main__":
    data1 = pandas.read_csv('mining(new).csv')
    data2 = pandas.read_csv('RQ3 ReadmeStatsByRanking(new).csv',
                       usecols=['name','user','readme','star', 'blocks', 'indents', 'images', 'links', 'lists', 'repo_size', 'language',
                                'license', 'average_update', 'Number_of_update', 'repo_created','readme_length','topic_score_sum','topic_score_average','topic_score_median','topic_score_max', 'total_days/update_freq'])
    data2 = data2[data2['repo_size'].notna()]
    print(data2[data2['total_days/update_freq'].isna()])
    data1 = data1.loc[:, ~data1.columns.str.match("Unnamed")]
    length = int(len(data2) * 0.2)
    bottom = data2.nsmallest(n=length, columns=['star'])
    top = data2.nlargest(n=length, columns=['star'])
    new_data = pandas.concat([top, bottom])
    print(len(new_data))
    data1['update_interval'] = new_data['total_days/update_freq'].to_list()
    data1 = data1.drop(['star','name','user','readme','repo_created','average_update', 'Number_of_update','topic_score_sum','topic_score_median','topic_score_max'], axis=1)
    print(data1[data1['update_interval'].isna()])
    data1.to_csv('rf_data(new).csv',index =False)