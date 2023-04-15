import os
import pandas

from RQ1.prune_related.prunning import valid
from RQ1.prune_related.one_contributor import getNonePersonal, get_more_than_one_year

"""
Remove readme file that contains a Default readme.
Other prunes are supported, change validation to do so
"""
if __name__ == '__main__':
    # load config
    invalid_length = 0
    invalid_language = 0
    invalid_heading = 0
    read_file = ""
    save_file = ""

    data = pandas.read_csv(read_file)
    data = data.dropna()
    # run basic prune
    for index, row in data.iterrows():
        readme = row['readme']
        validation = valid(readme, row['name'])
        if not validation[0]:
            data.drop(index, inplace=True)
            reason = validation[1]
            if reason == 0:
                invalid_length += 1
            elif reason == 1:
                invalid_language += 1
            elif reason == 2:
                invalid_heading += 1
    data = data.drop_duplicates(subset=['name', 'user'])
    print("Pruned:")
    print("Default README: %d" % invalid_length)
    print("README not in English: %d" % invalid_language)
    print("README with no heading: %d" % invalid_heading)
    invalid = data[data['readme'] == 'Missing README or Repo no long exists'].index
    data.drop(invalid, inplace=True)
    print("%d repos are invalid", len(data))
    data.to_csv(save_file, index=False)

    ##additional pruning
    get_more_than_one_year(read_file, save_file)
    getNonePersonal(read_file, save_file)
    print("complete")
