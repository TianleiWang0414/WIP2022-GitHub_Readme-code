import pandas

"""
Used just to see stats, can ignore
"""
if __name__ == "__main__":
    __file_name = ""
    data = pandas.read_csv(__file_name)
    sub_data = data.loc[data['star'] == 0]

    print(sub_data)
