import pandas
import datetime

"""
Additional prune criteria， 
"""


def getNonePersonal(read_file: str, save_file: str):
    data = pandas.read_csv(read_file)
    non_personal = data.loc[data['contributors'] > 1]

    print(non_personal.head)
    non_personal.to_csv(save_file, index=False)
    print(len(non_personal))


def get_more_than_one_year(read_file: str, save_file: str):
    curr = datetime.datetime.now()
    data = pandas.read_csv(read_file)
    data = data.dropna(subset=['repo_created'])
    for index, row in data.iterrows():
        created = row['repo_created'].split('T')[0].split('-')
        date = datetime.datetime(int(created[0]), int(created[1]), int(created[2]))
        diff = curr - date
        if diff.days < 365:
            data.drop(index, inplace=True)
    data.to_csv(save_file, index=False)
    print(len(data))
