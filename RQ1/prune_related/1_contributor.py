import pandas
import datetime
def getNonePersonal():
    data = pandas.read_csv("../popularity_repo.csv")
    non_personal = data.loc[data['contributors'] > 1]

    print(non_personal.head)
    non_personal.to_csv('non_personal_repo.csv', index=False)
    print(len(non_personal))

def get_more_than_one_year():
    curr = datetime.datetime.now()
    data = pandas.read_csv("../non_personal_repo.csv")
    data= data.dropna(subset=['repo_created'])
    for index,row in data.iterrows():


        created = row['repo_created'].split('T')[0].split('-')
        date = datetime.datetime(int(created[0]), int(created[1]), int(created[2]))
        diff = curr - date
        if diff.days < 365:
            data.drop(index,inplace = True)
    data.to_csv('new_data_set.csv',index = False)
    print(len(data))
if __name__ == '__main__':
    data = pandas.read_csv("../popularity_repo.csv")
    print(len(data))
    get_more_than_one_year()