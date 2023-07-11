import requests
from bs4 import BeautifulSoup as bs


def get_word(word):
    url = f'https://dictionary.cambridge.org/dictionary/english/{word.strip().lower()}'
    r = requests.get(url, allow_redirects=True, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    })
    if r.status_code == 200:
        return r.content
    return None


def get_translate(words):
    js_dict = {}
    error_list = []
    for word in words:
        if r_content := get_word(word):
            soup = bs(r_content, 'lxml')
            cambridge_answer = ''.join([i.text for i in soup.find('div', attrs={'class': 'def ddef_d db'})])
            js_dict[word] = cambridge_answer.replace(':', '').replace('\n', '')
        else:
            error_list.append(word)
    return save_to_file(js_dict, error_list)


def save_to_file(js_dict, error_words: list):
    with open('ans.txt', 'w') as f:
        for key, translate in js_dict.items():
            f.write(f'{key}\t{translate}\n')
    return [js_dict, error_words]


if __name__ == '__main__':
    get_translate(['couch'])
