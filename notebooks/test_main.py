import pytest
from main import train, predict
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

if __name__ == "__main__":
    pytest.main()