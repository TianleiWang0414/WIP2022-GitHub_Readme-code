import pandas as pd


def get_popular(data: pd.DataFrame, IncludeOutliers: bool) -> pd.DataFrame:
    popular = data.loc[data['star'] != 0]
    
    if not IncludeOutliers:
        return popular
    else:
        # use mean + 3 detal as the threshold for outliers detection
        
        mean = popular['star'].mean()
        sd = popular['star'].std()
        thres = mean + 3*sd
        return popular.loc[ popular['star']<thres]

def get_outlier_from_popular(data: pd.DataFrame):

    popular = data.loc[data['star'] != 0]
    # use mean + 3 detal as the threshold for outliers detection
    mean = popular['star'].mean()
    sd = popular['star'].std()
    thres = mean + 3*sd
    return popular.loc[popular['star']>thres]


def get_non_popular(data: pd.DataFrame) -> pd.DataFrame:
    return data.loc[data['star'] == 0]


def load_data(__file_name ):
    #__file_name =  "D:/paper/WIP2022-GitHub_Readme-code/data/all_in_one_data.csv"
    data = pd.read_csv(__file_name)
    # return repo which is not for software 
    data = data[data['language'] != 'None_language']
    print(data.shape)
    return data




# investigate on outliers
__file_name =  "D:/paper/WIP2022-GitHub_Readme-code/data/all_in_one_data.csv"
data_raw = pd.read_csv(__file_name,
                    usecols=['name', 'user', 'readme', 'star', 'blocks', 'indents', 'images', 'links', 'lists',
                            'language',
                            'license', 'readme_length', 'topic_score_average', 'update_interval', 'prob_popular',
                            'label', 'badge_count', 'Number_of_update'])

data_raw['language'].fillna('None_language', inplace=True)
data_raw['license'].fillna('None_license', inplace=False)

# assign new label
popular = get_popular(data_raw,True)
non_popular = get_non_popular(data_raw)
outliers = get_outlier_from_popular(data_raw)

##get statistics of outliers

print(outliers['readme_length'].mean())
print(outliers['links'].mean())
print(outliers['lists'].mean())
print(outliers['images'].mean())
print(outliers['Number_of_update'].mean())
print(outliers['update_interval'].mean())