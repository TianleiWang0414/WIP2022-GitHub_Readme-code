import pandas
from wordcloud import WordCloud
import json
import spacy
import ast
import matplotlib.pyplot as plt
if __name__ =='__main__':

    with open('message.json') as file:
        message_file = json.load(file)
        print(len(message_file))

    nlp = spacy.load("en_core_web_lg")
    text = " "
    print(message_file)
    for repo in message_file:
        for elements in repo:
            if type(elements) is str:
                doc = nlp(elements)
                for token in doc:
                    text += token.lemma_+ " "
            elif type(elements) is list:
                for message in elements:
                    doc = nlp(message)
                    for token in doc:
                        text += token.lemma_ + " "




    print(text)


    wordcloud =WordCloud(stopwords=nlp.Defaults.stop_words,background_color="white",collocations=False).generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()