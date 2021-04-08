from bs4 import BeautifulSoup
import requests, time
from requests import Session

url='https://ipsi.jinhak.or.kr/module/susi/univ/susiRltListAjax.do'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'Host':'ipsi.jinhak.or.kr',
    'Cookie':'IPSI=Raw1eGfTq4Xw2rO9TAubug1KCZSnq9OMLhtMDSV6op3EDyOYJ1x7Tof3k00tUab4.amV1c19kb21haW4vc2VydmVyNQ=='
    
}
payload={
    'page_now': '1',
}

session = Session()
session.head(url)
text = ''
for i in range(159420):
    payload['page_now'] = str(i+1)
    print(i+1)
    r = session.get(url,params=payload, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    f = open("test.csv", "a", encoding='utf-8')
    for x in soup.find_all('td'):
        if x.has_attr('scope'):
            print(text)
            f.write(text+'\n')
            text = x.get_text()
        else:
            text += ',' + x.get_text();
    time.sleep(0.2)
print(text)
f.write(text+'\n')
f.close()