from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests


def get_html(_url_):
    head = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'refere': 'https://example.com',
        'cookie': """your cookie value ( you can get that from your web page) """
    }
    req = Request(_url_)
    return urlopen(req).read()


url2 = 'https://cc.dinus.ac.id/lowongan/daftar'
url = 'https://food.grab.com/id/id/restaurant/ayam-geprek-abah-gaul-klaling-delivery/6-CYXJTNXTVVJWEA'
r = requests.get(url2, verify=False).text
print(r)
# the_html = get_html(url2)
# soup = BeautifulSoup(the_html, 'html.parser')
# for lk in soup.find_all('div', {'class': 'col-lg-3 col-md-6 col-12 mb-3'}):
#     print(lk)
