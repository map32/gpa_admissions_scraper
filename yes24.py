from bs4 import BeautifulSoup
import requests, time, json
from requests import Session

url='http://www.yes24.com/24/Category/Display/001001013003003?GS=03&FetchSize=100'
url2='http://www.yes24.com/Product/Goods/'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'Host':'www.yes24.com',
    
}
payload={
    'page_now': '1',
}

session = Session()
session.head(url)
text = ''
f = open("books.csv", "a", encoding='utf-8')
ff = open("chapters.csv", "a", encoding='utf-8')
for i in range(100):
    r = session.get(url+'&PageNumber='+str(i+1),params=payload, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    a = soup.find_all('div', class_='cCont_listArea')
    a = a[0].find("ul" , recursive=False).findChildren('li', recursive=False)
    if len(a) == 0:
        break
    print (str(i+1)+' found')
    for index, item in enumerate(a):
        values = json.loads(item.find('input', {'name':'ORD_GOODS_OPT'})['value'])
        code = str(values['goods_no'])
        name = values['goods_name']
        f.write(code+',"'+name+'"\n')
        r = session.get(url2+code, headers=headers)
        strip = r.text.replace('<br/>','\n')
        soup = BeautifulSoup(strip, 'html.parser')
        if (soup.find('h4', text='목차') == None):
            print(str(index)+' of page'+str(i+1)+' successful, no chapters')
            continue
        chapters = soup.find('h4', text='목차').parent.find_next_sibling("div").find('textarea').get_text().strip().splitlines()
        for chapter in chapters:
            if (len(chapter) > 0):
                ff.write(code+',"'+chapter+'"\n')
        print(str(index)+' of page'+str(i+1)+' successful')
f.close()
ff.close()