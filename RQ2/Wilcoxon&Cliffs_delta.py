from scipy.stats import ranksums
from cliffs_delta import cliffs_delta
import pandas as pd

if __name__ == '__main__':
    __file_name = ""
    data = pd.read_csv(__file_name)

    # split our data into popular and non popular
    popular = data.loc[data['star'] != 0]
    non_popular = data.loc[data['star'] == 0]
    popular = popular.drop(popular[popular.average_update == -1].index)
    non_popular = non_popular.drop(non_popular[non_popular.average_update == -1].index)
    sample1 = popular['star'].to_list()
    sample2 = non_popular['star'].to_list()
    print("========Wilcoxon rank-sum========")

    print('%%%Control variables%%%')
    print("Star: %s" % str(ranksums(sample1, sample2)))
    print("language: %s" % str(ranksums(popular['language'].to_list(), non_popular['language'].to_list())))
    print("License: %s" % str(ranksums(popular['license'].to_list(), non_popular['license'].to_list())))
    print("Repo_size: %s" % str(ranksums(popular['repo_size'].to_list(), non_popular['repo_size'].to_list())))
    print("Repo_created: %s" % str(ranksums(popular['repo_created'].to_list(), non_popular['repo_created'].to_list())))
    print("Topic_score_sum: %s" % str(
        ranksums(popular['topic_score_sum'].to_list(), non_popular['topic_score_sum'].to_list())))
    print("Topic_score_average: %s" % str(
        ranksums(popular['topic_score_average'].to_list(), non_popular['topic_score_average'].to_list())))
    print("Topic_score_median: %s" % str(
        ranksums(popular['topic_score_median'].to_list(), non_popular['topic_score_median'].to_list())))
    print("Topic_score_max: %s" % str(
        ranksums(popular['topic_score_max'].to_list(), non_popular['topic_score_max'].to_list())))

    print('%%%Investigating variable%%%')
    print("Blocks: %s" % str(ranksums(popular['blocks'].to_list(), non_popular['blocks'].to_list())))
    print("Indents: %s" % str(ranksums(popular['indents'].to_list(), non_popular['indents'].to_list())))
    print("Images: %s" % str(ranksums(popular['images'].to_list(), non_popular['images'].to_list())))
    print("Links: %s" % str(ranksums(popular['links'].to_list(), non_popular['links'].to_list())))
    print("lists: %s" % str(ranksums(popular['lists'].to_list(), non_popular['lists'].to_list())))
    print("Average_update: %s" % str(
        ranksums(popular['average_update'].to_list(), non_popular['average_update'].to_list())))
    print("Number_of_update: %s" % str(
        ranksums(popular['Number_of_update'].to_list(), non_popular['Number_of_update'].to_list())))
    print("Readme_length: %s" % str(
        ranksums(popular['readme_length'].to_list(), non_popular['readme_length'].to_list())))

    print("========Cliffs Delta========")
    print('%%%Control variables%%%')
    print("Star: %s" % str(cliffs_delta(sample1, sample2)))
    print("language: %s" % str(cliffs_delta(popular['language'].to_list(), non_popular['language'].to_list())))
    print("License: %s" % str(cliffs_delta(popular['license'].to_list(), non_popular['license'].to_list())))
    print("Repo_size: %s" % str(cliffs_delta(popular['repo_size'].to_list(), non_popular['repo_size'].to_list())))
    print("Repo_created: %s" % str(
        cliffs_delta(popular['repo_created'].to_list(), non_popular['repo_created'].to_list())))
    print("Topic_score_sum: %s" % str(
        cliffs_delta(popular['topic_score_sum'].to_list(), non_popular['topic_score_sum'].to_list())))
    print("Topic_score_average: %s" % str(
        cliffs_delta(popular['topic_score_average'].to_list(), non_popular['topic_score_average'].to_list())))
    print("Topic_score_median: %s" % str(
        cliffs_delta(popular['topic_score_median'].to_list(), non_popular['topic_score_median'].to_list())))
    print("Topic_score_max: %s" % str(
        cliffs_delta(popular['topic_score_max'].to_list(), non_popular['topic_score_max'].to_list())))

    print('%%%Investigating variable%%%')
    print("Blocks: %s" % str(cliffs_delta(popular['blocks'].to_list(), non_popular['blocks'].to_list())))
    print("Indents: %s" % str(cliffs_delta(popular['indents'].to_list(), non_popular['indents'].to_list())))
    print("Images: %s" % str(cliffs_delta(popular['images'].to_list(), non_popular['images'].to_list())))
    print("Links: %s" % str(cliffs_delta(popular['links'].to_list(), non_popular['links'].to_list())))
    print("lists: %s" % str(cliffs_delta(popular['lists'].to_list(), non_popular['lists'].to_list())))
    print("Average_update: %s" % str(
        cliffs_delta(popular['average_update'].to_list(), non_popular['average_update'].to_list())))
    print("Number_of_update: %s" % str(
        cliffs_delta(popular['Number_of_update'].to_list(), non_popular['Number_of_update'].to_list())))
    print("Readme_length: %s" % str(
        cliffs_delta(popular['readme_length'].to_list(), non_popular['readme_length'].to_list())))
    print("Badge_count: %s" % str(
        cliffs_delta(popular['badge_count'].to_list(), non_popular['badge_count'].to_list())))
    print("update_interval: %s" % str(
        cliffs_delta(popular['update_interval'].to_list(), non_popular['update_interval'].to_list())))

    print("\nBasic Stats")
    print("Star:  mean -> %f median->%s min->%f max->%f" % (
    popular['star'].mean(), popular['star'].median(), popular['star'].min(), popular['star'].max()))
    print("repo size:  mean -> %f median->%s min->%f max->%f" % (
        popular['repo_size'].mean(), popular['repo_size'].median(), popular['repo_size'].min(),
        popular['repo_size'].max()))
    print("Repo_created:  mean -> %f median->%s min->%f max->%f" % (
        popular['repo_created'].mean(), popular['repo_created'].median(), popular['repo_created'].min(),
        popular['repo_created'].max()))
    print("Topic_score_sum:  mean -> %f median->%s min->%f max->%f" % (
        popular['topic_score_sum'].mean(), popular['topic_score_sum'].median(), popular['topic_score_sum'].min(),
        popular['topic_score_sum'].max()))
    print("Topic_score_average:  mean -> %f median->%s min->%f max->%f" % (
        popular['topic_score_average'].mean(), popular['topic_score_average'].median(),
        popular['topic_score_average'].min(),
        popular['topic_score_average'].max()))

    print("Topic_score_median:  mean -> %f median->%s min->%f max->%f" % (
        popular['topic_score_median'].mean(), popular['topic_score_median'].median(),
        popular['topic_score_median'].min(),
        popular['topic_score_median'].max()))

    print("Topic_score_max:  mean -> %f median->%s min->%f max->%f" % (
        popular['topic_score_max'].mean(), popular['topic_score_max'].median(),
        popular['topic_score_max'].min(),
        popular['topic_score_max'].max()))

    print("Blocks:  mean -> %f median->%s min->%f max->%f" % (
        popular['blocks'].mean(), popular['blocks'].median(),
        popular['blocks'].min(),
        popular['blocks'].max()))

    print("Indents:  mean -> %f median->%s min->%f max->%f" % (
        popular['indents'].mean(), popular['blocks'].median(),
        popular['indents'].min(),
        popular['indents'].max()))

    print("Images:  mean -> %f median->%s min->%f max->%f" % (
        popular['images'].mean(), popular['images'].median(),
        popular['images'].min(),
        popular['images'].max()))

    print("Links:  mean -> %f median->%s min->%f max->%f" % (
        popular['links'].mean(), popular['links'].median(),
        popular['links'].min(),
        popular['links'].max()))

    print("Lists:  mean -> %f median->%s min->%f max->%f" % (
        popular['lists'].mean(), popular['lists'].median(),
        popular['lists'].min(),
        popular['lists'].max()))

    print("Average_update:  mean -> %f median->%s min->%f max->%f" % (
        popular['average_update'].mean(), popular['average_update'].median(),
        popular['average_update'].min(),
        popular['average_update'].max()))
    print("Average_update_(age/updates):  mean -> %f median->%s min->%f max->%f" % (
        popular['update_interval'].mean(), popular['update_interval'].median(),
        popular['update_interval'].min(),
        popular['update_interval'].max()))
    print("Number_of_update:  mean -> %f median->%s min->%f max->%f" % (
        popular['Number_of_update'].mean(), popular['Number_of_update'].median(),
        popular['Number_of_update'].min(),
        popular['Number_of_update'].max()))

    print("Readme_length:  mean -> %f median->%s min->%f max->%f" % (
        popular['readme_length'].mean(), popular['readme_length'].median(),
        popular['readme_length'].min(),
        popular['readme_length'].max()))
    print("Badge_count:  mean -> %f median->%s min->%f max->%f" % (
        popular['badge_count'].mean(), non_popular['badge_count'].median(),
        popular['badge_count'].min(),
        popular['badge_count'].max()))
    print("time_since_last_update:  mean -> %f median->%s min->%f max->%f" % (
        popular['time_since_last_update'].mean(), popular['time_since_last_update'].median(),
        popular['time_since_last_update'].min(),
        popular['time_since_last_update'].max()))
    print("time_since_last_update: %s" % str(
        cliffs_delta(popular['time_since_last_update'].to_list(), non_popular['time_since_last_update'].to_list())))

    #####
    print("\nNon-popular group")
    print("Star:  mean -> %f median->%s min->%f max->%f" % (
        non_popular['star'].mean(), non_popular['star'].median(), non_popular['star'].min(), non_popular['star'].max()))
    print("repo size:  mean -> %f median->%s min->%f max->%f" % (
        non_popular['repo_size'].mean(), non_popular['repo_size'].median(), non_popular['repo_size'].min(),
        non_popular['repo_size'].max()))
    print("Repo_created:  mean -> %f median->%s min->%f max->%f" % (
        non_popular['repo_created'].mean(), non_popular['repo_created'].median(), non_popular['repo_created'].min(),
        non_popular['repo_created'].max()))
    print("Topic_score_sum:  mean -> %f median->%s min->%f max->%f" % (
        non_popular['topic_score_sum'].mean(), non_popular['topic_score_sum'].median(),
        non_popular['topic_score_sum'].min(),
        non_popular['topic_score_sum'].max()))
    print("Topic_score_average:  mean -> %f median->%s min->%f max->%f" % (
        non_popular['topic_score_average'].mean(), non_popular['topic_score_average'].median(),
        non_popular['topic_score_average'].min(),
        non_popular['topic_score_average'].max()))

    print("Topic_score_median:  mean -> %f median->%s min->%f max->%f" % (
        non_popular['topic_score_median'].mean(), non_popular['topic_score_median'].median(),
        non_popular['topic_score_median'].min(),
        non_popular['topic_score_median'].max()))

    print("Topic_score_max:  mean -> %f median->%s min->%f max->%f" % (
        non_popular['topic_score_max'].mean(), non_popular['topic_score_max'].median(),
        non_popular['topic_score_max'].min(),
        non_popular['topic_score_max'].max()))

    print("Blocks:  mean -> %f median->%s min->%f max->%f" % (
        non_popular['blocks'].mean(), non_popular['blocks'].median(),
        non_popular['blocks'].min(),
        non_popular['blocks'].max()))

    print("Indents:  mean -> %f median->%s min->%f max->%f" % (
        non_popular['indents'].mean(), non_popular['blocks'].median(),
        non_popular['indents'].min(),
        non_popular['indents'].max()))

    print("Images:  mean -> %f median->%s min->%f max->%f" % (
        non_popular['images'].mean(), non_popular['images'].median(),
        non_popular['images'].min(),
        non_popular['images'].max()))

    print("Links:  mean -> %f median->%s min->%f max->%f" % (
        non_popular['links'].mean(), non_popular['links'].median(),
        non_popular['links'].min(),
        non_popular['links'].max()))

    print("Lists:  mean -> %f median->%s min->%f max->%f" % (
        non_popular['lists'].mean(), non_popular['lists'].median(),
        non_popular['lists'].min(),
        non_popular['lists'].max()))

    print("Average_update:  mean -> %f median->%s min->%f max->%f" % (
        non_popular['average_update'].mean(), non_popular['average_update'].median(),
        non_popular['average_update'].min(),
        non_popular['average_update'].max()))
    print("Average_update_(age/updates):  mean -> %f median->%s min->%f max->%f" % (
        non_popular['update_interval'].mean(), non_popular['update_interval'].median(),
        non_popular['update_interval'].min(),
        non_popular['update_interval'].max()))
    print("Number_of_update:  mean -> %f median->%s min->%f max->%f" % (
        non_popular['Number_of_update'].mean(), non_popular['Number_of_update'].median(),
        non_popular['Number_of_update'].min(),
        non_popular['Number_of_update'].max()))

    print("Readme_length:  mean -> %f median->%s min->%f max->%f" % (
        non_popular['readme_length'].mean(), non_popular['readme_length'].median(),
        non_popular['readme_length'].min(),
        non_popular['readme_length'].max()))

    print("Badge_count:  mean -> %f median->%s min->%f max->%f" % (
        non_popular['badge_count'].mean(), non_popular['badge_count'].median(),
        non_popular['badge_count'].min(),
        non_popular['badge_count'].max()))

    print("time_since_last_update:  mean -> %f median->%s min->%f max->%f" % (
        non_popular['time_since_last_update'].mean(), non_popular['time_since_last_update'].median(),
        non_popular['time_since_last_update'].min(),
        non_popular['time_since_last_update'].max()))
