import pandas
"""
You can use this to find subset in a bigger frame to save some time on GITHUB API
col_to_add -> cols you are intrested to add into a subset
"""
if __name__ == "__main__":
    sub_name = ""
    all_name = ""
    save_name = ""
    col_to_add = []
    entry = {}
    for col in col_to_add:
        entry[col] = []
    subset = pandas.read_csv(sub_name)
    allset = pandas.read_csv(all_name)

    for _, row in subset.iterrows():
        user = row['user']
        repo = row['name']

        cross_ref = allset.loc[(allset['user'] == user) & (allset['name'] == repo)]
        for col in col_to_add:
            entry[col].append(cross_ref[col].iloc[0])

    for i in col_to_add:
        subset[i] = entry[i]

    subset.to_csv(save_name, index=False)