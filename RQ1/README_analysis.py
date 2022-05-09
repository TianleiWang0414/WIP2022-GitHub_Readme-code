
import regex as re
import nltk
import pandas


include_word_count = False



# Regex expressions
code_regex = r'`{3}([\S\s]*?)`{3}.*'  # Regex to detect code block, same as in prunning.py
indent_code_regex = re.compile(r'^((?:(?:[ ]{4}|\t).*(\R|$))+)',
                               re.MULTILINE)  # code from indents https://stackoverflow.com/questions/41351903/how-can-i-match-a-markdown-code-block-with-regex
inline_code_regex = r'\`{1,}([^\`].*?)\`{1,}'  # Modified from https://stackoverflow.com/questions/41274241/how-to-capture-inline-markdown-code-but-not-a-markdown-code-fence-with-regex
link_regex = r'\[[^\]\r\n]+\]\([^\)\r\n]+\)'  # Obtained & Modified from https://davidwells.io/snippets/regex-match-markdown-links
image_regex = r'!\[[^\]\r\n]+\]\([^\)\r\n]+\)'  # Modification of the link_regex OLD image: !{1}\[([^\[]+)\](\(.*\))
lists_regex = re.compile(r'(^ {,3}(-|\+|\*|[0-9\.])+ [\S\s]*?\r\n\r\n)', re.MULTILINE)
header_regex = re.compile(r'(#+ )(.+)')  # Group 1 will return all headers

file_reader = pandas.read_csv("../RQ3/rank_repo.csv", usecols=['name', 'user', 'readme', 'star', 'rank_point', 'repo_size',
                                                        'language', 'repo_created','license'], encoding='UTF-8')
readme_files = file_reader['readme']
rank_rating = file_reader['rank_point']
star = file_reader['star']


blocks = []
indents = []
images = []
links = []
lists = []
num_words = []

# Types of keys we have in dictionary [content of readmes]
keys = ['blocks', 'indents', 'images', 'links', 'lists']  # inlines

# First, we begin with the basic stats of the structure of the readme from RQ1
# This time, we are tracking this based on their popularity
index = 0

for i in range(len(readme_files)):
    readme = readme_files[i]

    num_code_block = len(re.findall(code_regex, readme))

    # Now adjusting the readme so that we remove code blocks.
    # Links and images are not the same when inside of a code block [We don't want to match them as one]
    # Assure headers also don't get mixed with other things
    change = re.sub(code_regex, '<code block>', readme)
    change = re.sub(header_regex, '<header>', change)

    num_code_indent = len(re.findall(indent_code_regex, change))
    change = re.sub(indent_code_regex, '<code indent>', change)

    # num_code_inline = len(re.findall(inline_code_regex, change))
    # change = re.sub(inline_code_regex, '<inlined code>', change)

    num_code_snippets = num_code_block + num_code_indent  # + num_code_inline

    # Summarize the rest of the readme file
    num_images = len(re.findall(image_regex, change))
    change = re.sub(image_regex, '<image>', change)  # Assure links do not capture images

    num_links = len(re.findall(link_regex, change))
    change = re.sub(link_regex, '<link>', change)

    num_lists = len(re.findall(lists_regex, change))
    change = re.sub(lists_regex, '<list>', change)

    blocks.append(num_code_block)
    indents.append(num_code_indent)
    images.append(num_images)
    links.append(num_links)
    lists.append(num_lists)

    readme_no_lines = change.replace("\r\n", " ").strip()

    if include_word_count:
        tot_words = 0

        # Count number of words in dictionary
        for word in readme_no_lines.split():
            if word in nltk.corpus.words.words():
                tot_words += 1

        num_words.append(tot_words)

    index += 1
    if index % 50 == 0:
        print('Progress report, completed: ' + str(index))

df3 = pandas.DataFrame({'blocks': blocks})
df4 = pandas.DataFrame({'indents': indents})
df5 = pandas.DataFrame({'images': images})
df6 = pandas.DataFrame({'links': links})
df7 = pandas.DataFrame({'lists': lists})
df8 = pandas.DataFrame({'words': num_words})

dataFrames = [ df3, df4, df5, df6, df7, df8]



finalResult = pandas.concat(dataFrames, axis=1)
concatResult = pandas.concat([file_reader,finalResult,], axis=1)

print(concatResult.head())
# Write results to file so we do not need to run this again
concatResult.to_csv('RQ3 ReadmeStatsByRanking.csv', encoding='utf-8',index= False)

print(str(len(readme_files)))
