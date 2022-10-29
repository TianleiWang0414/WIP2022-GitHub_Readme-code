import os
import re
import spacy
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd

from nltk.stem import PorterStemmer
from ast import literal_eval

"""
This file generate popular and non popular groups and extract the header information for each
csv file is required to have star and readme col

Run following to get the required data:
data_retrieval_readme.py
data_retrieval_stats.py
"""
heading_regex = "#+ .+\\s"
code_regex = r'^```[^\S\r\n]*[a-z]*(?:\n(?!```$).*)*\n```'
code_flag = re.MULTILINE

def inCodeBlock(word_index: int, file: str) -> bool:
    inCode = False
    iterator = re.finditer(code_regex, file, code_flag)
    for match in iterator:
        range = match.span()
        if word_index >= range[0] and word_index < range[1]:
            inCode = True
            break
    return inCode

def getMiningData(file,name):
    nlp = spacy.load("en_core_web_lg")
    stemmer = PorterStemmer()
    popular_header = []
    for _, row in file.iterrows():
        readme = row['readme']
        headings = re.findall(heading_regex, readme)
        curr_header = []
        for header in headings:
            index = readme.find(header)
            if not inCodeBlock(index, readme):
                doc = nlp(header)
                for token in doc:
                    if token.is_alpha and not token.is_stop:

                        stemmed = stemmer.stem(token.lemma_.lower())
                        print(stemmed)
                        curr_header.append(stemmed)
        popular_header.append(curr_header)
    P_dataframe = pd.DataFrame({'Header': popular_header})
    P_dataframe.to_csv(name, index=False)
def doMining(file,name):
    transact = []

    for _, row in file.iterrows():
        transact.append(row['Header'])

    te = TransactionEncoder()
    te_ary = te.fit(transact).transform(transact)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    print(df)
    mined = fpgrowth(df, min_support=0.05, use_colnames=True)
    mined.to_csv(name, index=False)
if __name__ == '__main__':
    __file_name = ""
    __save_name = ""
    data = pd.read_csv(__file_name)

    # split our data into popular and non popular
    popular = data.loc[data['star'] != 0]
    non_popular = data.loc[data['star'] == 0]

    #if no header info
    if not os.path.isfile('popular_header.csv'):
        getMiningData(popular,'popular_header.csv')
    if not os.path.isfile('"mined_popular.csv"'):
        popular_header = pd.read_csv('popular_header.csv')
        popular_header.Header = popular_header.Header.apply(literal_eval)
        doMining(popular_header,"mined_popular.csv")

    # if no header info
    if not os.path.isfile('Non-popular_header.csv'):
        getMiningData(non_popular,'Non-popular_header.csv')
    if not os.path.isfile('"mined_popular.csv"'):
        non_popular = pd.read_csv('Non-popular_header.csv')
        non_popular.Header = non_popular.Header.apply(literal_eval)
        doMining(non_popular,"Non-mined_popular.csv")
