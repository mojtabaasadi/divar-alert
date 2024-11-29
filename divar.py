from email import header
from urllib import request
from bs4 import BeautifulSoup
import requests,os,time,random,json,codecs

URL = "https://divar.ir/s/{SEARCH_CONDITIONS}".format(**os.environ)
DISCORD_HOOK = os.environ.get("DISCORD_HOOK", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 
BOT_CHATID = os.environ.get('BOT_CHATID', "")

proxy_config = {}
if os.environ.get("HTTP_PROXY", ""):
    proxy_config["HTTP_PROXY"] = os.environ.get("HTTP_PROXY")
if os.environ.get("HTTPS_PROXY", ""):
    proxy_config["HTTPS_PROXY"] = os.environ.get("HTTPS_PROXY")


divar_session = requests.Session()
divar_session.headers = {
    **divar_session.headers,
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Accept':'application/json, text/plain, */*',
    'Accept-Language':'en-US,en;q=0.5',
    'Accept-Encoding':'gzip, deflate, br',
    'Referer':'https://divar.ir/',
    'Origin':'https://divar.ir',
    'Connection':'keep-alive',
    'Sec-Fetch-Dest':'empty',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Site':'same-site',
    'Pragma':'no-cache',
    'Cache-Control':'no-cache',
    'TE':'trailers',
}


def send_telegram_message(title,link):
    url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
    text = f"<b>{title}</b>" + "\n" +link
    body = {"chat_id": BOT_CHATID, "parse_mode": "HTML", "text": text}
    try:
        result = requests.post(url, data=body, proxies=proxy_config)
        if result.status_code == 429:
            time.sleep(random.randint(3, 7))
            send_telegram_message(title, link)
    except Exception as e:
        print(e)

def send_discrod_message(content):
    data = {
        "content" : content,
        "username" : "from divar"
    }
    result = requests.post(DISCORD_HOOK, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))


def main():
    with codecs.open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'prev.txt'),'a+','utf8') as prev:
        prev.seek(0)
        sent = prev.read()
        tosend = []
        r= divar_session.get(URL)
        posts = []
        try:
            data = r.text
            r.soup = BeautifulSoup(data, 'html.parser')
            json_text = soup.find_all('script',type= "application/ld+json")[-1].get_text()
            posts = json.loads(json_text)
        except Exception as e:
            print(e)
        for ad in posts:
            url = ad['url']
            title = ad['name']
            if sent.find(url)==-1:
                if len(DISCORD_HOOK):
                    send_discrod_message(title +'\n'+url)
                if len(BOT_TOKEN):
                    send_telegram_message(title,url)
                tosend.append(url)
        prev.write('\n'+'\n'.join(tosend))
        prev.close()

if __name__ == '__main__':
    main()
