import pandas

from RQ1.prunning import valid

if __name__ == "__main__":
    invalid_length = 0
    invalid_language = 0
    invalid_heading = 0
    data = pandas.read_csv("additional_DataWithReadme.csv")
    data = data.dropna(how='any',axis=0)
    for index, row in data.iterrows():
        print(index)
        readme = row['readme']
        validation = valid(readme)
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
    print("README too short: %d" % (invalid_length))
    print("README not in English: %d" % (invalid_language))
    print("README with no heading: %d" % (invalid_heading))
    old= pandas.read_csv('cleaned_data.csv',usecols=['name','user','readme'],)
    old= old.append(data, ignore_index=True)
    #old.to_csv("cleaned_data.csv",index=False)