import re
import pandas

image_regex = re.compile(r'!\[[^\]\r\n]+\]\([^\)\r\n]+\)')
badge_website = ["https://img.shields.io"]
"""
This file add badge info to a pandaframe
input csv file is required to have a col name readme to extract such info. Run data_retrieval_readme
beforehand
"""
if __name__ == "__main__":
    __file_name = ""
    __save_name = ""

    data = pandas.read_csv(__file_name)
    badge_counts = []
    badge_action = []
    for _, row in data.iterrows():
        readme = row['readme']
        possible_badge = re.findall(image_regex, readme)
        badge_count = 0
        badge_names = []
        for img in possible_badge:
            for web_page in badge_website:
                if web_page not in img:
                    continue
                print(img)
                badge_count += 1
                start_index = img.find('[')
                end_index = img.find(']')
                if start_index + 1 < end_index:
                    badge_names.append(img[start_index + 1:end_index])

        badge_action.append(badge_names)
        badge_counts.append(badge_count)
        print(badge_names)
        print(badge_count)
    data['badge_info'] = badge_action
    data['badge_count'] = badge_counts

    data.to_csv(__save_name, index= False)
