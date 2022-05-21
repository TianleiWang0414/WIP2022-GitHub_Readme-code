import numpy as np
import pandas
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_predict, KFold, cross_val_score

if __name__ == '__main__':
    pop_header = pandas.read_csv('popular_header.csv')
    non_pop_header =pandas.read_csv('Non-popular_header.csv')
    empty = non_pop_header.loc[non_pop_header['Header']=='[]']
    print(len(empty)/len(non_pop_header))
    high_label = [1] * len(pop_header)
    low_label =[0] * len(non_pop_header)
   # print(high_label)
    pop_header['label'] =high_label
    non_pop_header['label'] = low_label

    data = []
    for _,row in pop_header.iterrows():
        header = row['Header']
        s = ' '.join(header)
        data.append(header)
    for _,row in non_pop_header.iterrows():
        header = row['Header']
        s = ' '.join(header)
        data.append(header)
    pop_header= pop_header.append(non_pop_header)

    print(pop_header)
    vectorizer = CountVectorizer(analyzer="word",
                                 tokenizer=None,
                                 preprocessor=None,
                                 stop_words=None,
                                 max_features=100000)
    X_test = vectorizer.fit_transform(data)
    X_test = X_test.toarray()
    print(len(X_test))
    vocab = vectorizer.get_feature_names_out()
    print(vocab)
    rf = RandomForestClassifier(n_estimators=200)
    cv = KFold(n_splits=10)

    pop_header = pop_header.sample(frac=1).reset_index(drop=True)
    #proba = cross_val_predict(rf,X_test,pop_header['label'],cv=cv, method='predict_proba')
    score_a = cross_val_score(rf, X_test, pop_header['label'], cv=cv, scoring='accuracy')
    score_r = cross_val_score(rf, X_test, pop_header['label'], cv=cv, scoring='recall')
    score_p = cross_val_score(rf, X_test, pop_header['label'], cv=cv, scoring='precision')

    print("10-folds\n accuracy: %s\n recall: %s\n precision: %s\n" % (
        np.mean(score_a), np.mean(score_r), np.mean(score_p)))
    print(proba)

    prob = [x[1] for x in proba]

    save = pandas.read_csv('mining.csv')
    save['prob_popular'] =prob
    save.to_csv('mining(new).csv')