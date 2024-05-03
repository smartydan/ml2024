import pytest
from main import train, predict, split_f, preprocess
from submain import rm_punc, rm_stopwords
import os
import errno

def test_invalid_train(capsys):
    model = "model_test.pkl"
    if os.path.exists(model):
        os.remove(model)
    data = "../data/singapoor_airlines_reviews.csv"
    with pytest.raises(Exception) as err_info:
        train(['--data', data, '--model', model], standalone_mode=False)
    err = err_info.value
    print(err)
    assert err_info.type is FileNotFoundError
    # assert err == FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), data) # doesn't work this way
    assert not os.path.isfile(model)

def test_valid_train():
    model = "model_test.pkl"
    if os.path.exists(model):
        os.remove(model)
    data = "../data/singapore_airlines_reviews.csv"
    train(['--data', data, '--model', model], standalone_mode=False)
    assert os.path.isfile(model)

def test_predict(capsys):
    model = "model_test.pkl"
    data = "Very nice company"
    predict(['--data', data, '--model', model], standalone_mode=False)
    captured = capsys.readouterr()
    data = rm_punc(rm_stopwords(data))
    assert captured.out in [data + " " + str(i) + "\n" for i in range(1, 6)]
    os.remove(model)

def test_split_f(): # special ^)
    X, y = preprocess("../data/singapore_airlines_reviews.csv")
    split_factor = 0.2
    X_train, X_test, y_train, y_test = split_f(X, y, split_factor, 42)
    assert abs(X_test.shape[0] / (X_test.shape[0] + X_train.shape[0]) - split_factor) < 1e-5

def test_punctuation_func():
    text = "Ab.,.c!"
    assert rm_punc(text) == "abc"


if __name__ == "__main__":
    pytest.main()