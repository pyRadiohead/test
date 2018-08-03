import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
from bs4.element import Comment
import string
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head','meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True
def print_words(text):
    punctuation_symbols = string.punctuation + string.whitespace
    some_text = text.lower().split()
    dict = {}
    for word in some_text:
        word = word.strip(punctuation_symbols)
        if len(word) > 2 and word.isalpha():
            dict[word] = dict.get(word,0) + 1
    return dict

def print_top_words(text):
    words = print_words(text)
    for k, v in sorted(words.items(),key = lambda t: t[1],reverse=True)[:5]:
        print('{:20} {:5}'.format(k,v))

def text_from_html(soup):
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)
def print_titles_and_alts(soup):
    info = []
    for i in [i['alt'] for i in soup.find_all('img', alt=True)] + [i for i in soup.title]:
        info.append(i)
    print(info)

http = urllib3.PoolManager(retries = False)
r = open('words2.txt', 'r', encoding='utf-8')
website_list = r.read().split()
for url in website_list:
    try:
        timestamp_list = ['2000000000_id']
        for timestamp in timestamp_list:
            response = http.request('GET', 'http://web.archive.org/web/' + timestamp + '_id/http://www.'+url)
            soup = BeautifulSoup(response.data, 'html.parser')
            print(url)
            og_info = ""
            meta_name = ""
            for tag in soup.findAll("meta"):
                if tag.get('property',None) in ['og:title','og:description','og:keywords']:
                    og_info = tag['content'].strip()
                    print(tag.get('property',None)+'::',og_info)
                if tag.get('name',None) in ['title','description','keywords']:
                    meta_name = tag['content'].strip()
                    print(tag.get('name',None)+ '::', meta_name)
            if len(og_info) < 1 or len(meta_name)< 1:
                html_text = text_from_html(soup)
                print_titles_and_alts(soup)
                print(print_top_words(html_text))
        print("-"*19)
    except:
        pass



