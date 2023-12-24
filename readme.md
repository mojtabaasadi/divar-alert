
# Divar Alert (Telegram & Discoord)

Recieve alert when new ad gets published on divar. On telegram or discord or both

- set following envirment variables or change them in the code:`divar.py`
```
SEARCH_CONDITIONS: // link of divar search resaults without "https://divar.ir/s/" at the begining
BOT_TOKEN: // in case u want to recieve messages on telegram; get it from https://t.me/BotFather 
BOT_CHATID: // in case u want to recieve messages on telegram; your telegram user id ( get from https://t.me/getidsbot) after sending a message to the bot you've created 
HTTP_PROXY: // in case u want to recieve messages on telegram
HTTPS_PROXY: //in case u want to recieve messages on telegram
DISCORD_HOOK:// in case you want to recieve message on discord , guide:https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks
```

## As a docker container 
- you can run your container on https://liara.ir/
- or just build and run it on your server
```
docker build --rm -t my-test-bot .

docker run -d -t -i \
            -e "HTTP_PROXY=$HTTP_PROXY" \ 
            -e "HTTPS_PROXY=$HTTPS_PROXY" \ 
            -e "SEARCH_CONDITIONS=shiraz/rent-apartment?credit=50000000-90000000&size=-60&parking=true" \
            -e "BOT_TOKEN=$BOT_TOKEN" \
            -e "DISCORD_HOOK=$DISCORD_HOOK" \
            my-test-bot
```
