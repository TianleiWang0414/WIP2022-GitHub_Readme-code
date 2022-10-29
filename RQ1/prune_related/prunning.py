import re
import enchant
import pandas

__min_length = 2000
heading_regex = "#+ .+\\s"
code_regex = r'^```[^\S\r\n]*[a-z]*(?:\n(?!```$).*)*\n```'
code_flag = re.MULTILINE
from langdetect import detect

"""
checks the word is in a code block, word_index is the start index of a word or sentence
    you would need to use span to find the start index of the word/sentence
"""


def inCodeBlock(word_index: int, file: str) -> bool:
    inCode = False
    iterator = re.finditer(code_regex, file, code_flag)
    for match in iterator:
        range = match.span()
        if word_index >= range[0] and word_index < range[1]:
            inCode = True
            break
    return inCode


"""Is the readme default"""


def __word_length_check(file: str, repo_name: str) -> bool:
    default_readme = "# %s\n" % repo_name
    return default_readme != str(file)


"""Is the readme in English"""


def __English_check(file: str) -> bool:
    try:
        is_en = detect(file) == 'en'
        return is_en
    except:
        return False


"""check if heading is in readme and is in English"""


def __heading_check(file: str, dict: enchant.Dict) -> bool:
    headings = re.findall(heading_regex, file)
    __failCase = 0
    __totalCase = 0
    __ratio = 1
    # print(headings)
    for heading in headings:
        info = heading.replace("#", "")
        info = info.replace('\n', '')
        info = info.strip()
        for words in info.split(" "):
            try:
                inDict = dict.check(words)
                if not inDict:
                    __failCase += 1
            except ValueError:
                __failCase += 1
            finally:
                __totalCase += 1
    valid = len(headings) > 0
    if valid:
        __ratio = float(__failCase) / __totalCase
    return valid > 0 and __ratio <= .2


def valid(in_file: str, repo_name: str) -> (bool, int):
    d = enchant.Dict("en_US")
    return_int = -1
    return_bool = True
    if not __word_length_check(in_file, repo_name):
        return_int = 0
        return_bool = False
    elif not __English_check(in_file):
        return_int = 1
        return_bool = False
    # elif not __heading_check(file, d):
    #   return_int = 2
    #   return_bool = False
    return return_bool, return_int


def example():
    file = """## Step 5 Show results

```python
# generate a simulation summary,
# and save the summary and all data in directory './data'.
# You can specify the directory.
sim.results('./data/')

# generate a simulation summary, do not save any file
sim.results()

# plot interested data
sim.plot(['ref_pos', 'gyro'], opt={'ref_pos': '3d'})
```

# Acknowledgement
"""
    index_true = file.find("# generate a simulation summary")
    headings = re.findall(heading_regex, file)

    for header in headings:
        index = file.find(header)
        if not inCodeBlock(index, file):
            print(header)
    print(headings)
    index_false = file.find("## Step 5 Show results")
    in_code = inCodeBlock(index_true, file)
    print("# generate a simulation summary is in a code block \nexpect: True\nreturn: %s" % (in_code))
    in_code = inCodeBlock(index_false, file)
    print("## Step 5 Show results is not in a code block \nexpect: False\nreturn: %s" % (in_code))


"""
This main is used for stats, use prune_main.py for actual prune
"""
if __name__ == "__main__":
    # example()
    d = enchant.Dict("en_US")
    file = pandas.read_csv('dataWithREADME.csv')
    file = file.drop_duplicates()
    invalid = file[file['readme'] == 'Missing README or Repo no long exists'].index
    file.drop(invalid, inplace=True)
    print(len(file))
    total = 0
    for index, row in file.iterrows():

        if valid(row['readme'], row['name'])[1] == 1:
            # print(row['readme'])
            total += 1
    print(total)
