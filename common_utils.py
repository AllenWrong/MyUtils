import requests
import json
import pickle


def get_remote_txt(address, parse_fn=None):
    """get remove .txt file and use parse_fn to parse content."""
    response = requests.get(address)
    if response.status_code == 200:
        if parse_fn is not None:
            return parse_fn(response.text)
    else:
        print("can not accesss!")
        return None


def parse_git_repo(response_text):
    """parse github reposity txt file"""
    return json.loads(response_text)['payload']['blob']['rawLines']


def save_sk_model(model, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(model, f)


def load_sk_model(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)