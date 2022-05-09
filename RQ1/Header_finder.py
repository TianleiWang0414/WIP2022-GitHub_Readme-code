
import re
import spacy
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd
from nltk.stem import PorterStemmer
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