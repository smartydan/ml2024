import click
import os
import pandas as pd
import errno
from submain import *

@click.group()
def main():
    pass

@click.command()
@click.option('--data', required=True, help="Data to train on.")
@click.option('--model', required=True, help="Path to save model to")
@click.option('--test', required=False, help="Data to test on. Shouldn't be passed with split together.")
@click.option('--split', required=False, type=float, help="If passed, data will be split into two parts, (split) test and (1 - split) train.")
def train(data, model, test=None, split=None):
    print('You called train function')
    assert not (test and split), "train and split shouldn't be specified together"
    if not os.path.exists(data):
         raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), data)
    
    df = pd.read_csv(data)
    df['title_text'] = (df['title'] + ' '  + df['text']).apply(rm_punc)
    df['clean'] = df['title_text'].apply(rm_stopwords)
    df['clean'] = df['clean'].apply(func)

    svc = SVC()
    vectorizer = TfidfVectorizer()

    X = df.clean
    y = df.rating

    x_test = y_test = None
    
    if split:
        assert 0 <= split <= 1, "split size should be between 0 and 1"
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=split, random_state=RANDOM_STATE)
        x_train = vectorizer.fit_transform(x_train)
        x_test = vectorizer.transform(x_test)
        svc.fit(x_train, y_train)
    else:
        X = vectorizer.fit_transform(X)
        svc.fit(X, y)

    if test:
        assert os.path.exists(test), "pass valid test path"
        df_test = pd.read_csv(test)
        df_test['title_text'] = (df_test['title'] + ' '  + df_test['text']).apply(rm_punc)
        df_test['clean'] = df_test['title_text'].apply(rm_stopwords)
        x_test = df_test.clean
        y_test = df_test.rating

        x_test = vectorizer.transform(x_test)

    if x_test is not None:
        y_pred = svc.predict(x_test)
        print("Metrcis are: ")
        print(classification_report(y_test, y_pred))
        
    print(f"Model fited and will be saved now to {model}")
    save(svc, model)
    save(vectorizer, model + "_")

@click.command()
@click.option('--data', required=True, help="Data to predict on. Either path to csv file, or string in format <text | target>")
@click.option('--model', required=True, help="Path to save model to")
def predict(data, model):
    svc = load(model)
    vectorizer = load(model + "_")
    
    if os.path.exists(data):
        df = pd.read_csv(data)[:10]
        df['title_text'] = (df['title'] + ' '  + df['text']).apply(rm_punc)
        df['clean'] = df['title_text'].apply(rm_stopwords)
    
        data = df.clean
        y = df.rating
        X = vectorizer.transform(data)
        
        y_pred = svc.predict(X)
        for text, score in zip(data, y_pred):
            print(text, score, sep="\n", end="\n\n--------\n")

    else:
        data = rm_punc(data)
        data = rm_stopwords(data)
        X = vectorizer.transform([data])
        y_pred = svc.predict(X)[0]
        print(data, y_pred)


main.add_command(train)
main.add_command(predict)

if __name__ == '__main__':
    main()
