import pandas
pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)
if __name__ == '__main__':
    update_info = pandas.read_csv('RQ3 ReadmeStatsByRanking.csv')
    readme_length = []

    for _,row in update_info.iterrows():
        readme_length.append(len(row['readme']))

    update_info['readme_length'] = readme_length


    update_info.to_csv('RQ3 ReadmeStatsByRanking.csv',index= False)
