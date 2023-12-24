from email import header
from urllib import request
from bs4 import BeautifulSoup
import requests,os,time,random

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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type':'text/html; charset=utf-8',
    'Origin': 'https://divar.ir',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Referer': 'https://divar.ir/',
    'Connection': 'keep-alive',
    'Cookie': 'did=250dfd5c-8c63-4a38-b770-92ee16bdb6e6; _ga=GA1.1.2019623298.1642936967; multi-city=shiraz%7C; city=shiraz; _gcl_au=1.1.710975817.1654779139; _ga_SXEW31VJGJ=GS1.1.1659170439.5.1.1659170749.0; token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMDkzNTA4MjMwMjMiLCJpc3MiOiJhdXRoIiwiaWF0IjoxNjU5MTcwNDQwLCJleHAiOjE2NjA0NjY0NDAsInZlcmlmaWVkX3RpbWUiOjE2NTg3MjkwNzQsInVzZXItdHlwZSI6InBlcnNvbmFsIiwidXNlci10eXBlLWZhIjoiXHUwNjdlXHUwNjQ2XHUwNjQ0IFx1MDYzNFx1MDYyZVx1MDYzNVx1MDZjYyIsInNpZCI6IjRmMzdlMjEzLTU1N2ItNDViYS1hMzU1LTA1NWFjNTJkYWMwZSJ9.Uw1xtn9-2VBOxD3mtlEN7gsoubKG4OmmM9Pzc7hPOD0; _gid=GA1.2.491932182.1659170440; _gat_gtag_UA_32884252_2=1',
    'TE': 'trailers'
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
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'prev.txt'),'a+') as prev:
        prev.seek(0)
        sent = prev.read()
        tosend = []
        r= divar_session.get(URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        for ad in soup.select('.virtual-infinite-scroll [class^=post-card-item]'):
            code = ad.select('div>a')[0].get('href').split('/')[-1]
            title = ad.select_one('h2').get_text()
            url = 'https://divar.ir/v/'+code
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
