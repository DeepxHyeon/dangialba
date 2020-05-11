import requests
import os
import telegram
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

bot = telegram.Bot(token='token')
chat_id = chat_id

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def job_function():
    html = requests.get('url')
    html.encoding = 'euc-kr'
    soup = BeautifulSoup(html.text, 'html.parser')
    posts = soup.select('p.cTit')
    latest = posts[0].text

    with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+') as f_read:
        before = f_read.readline()
        f_read.close()
        if before != latest:
            bot.sendMessage(chat_id=chat_id, text=latest+' \nurl')
            with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write:
                f_write.write(latest)
                f_write.close()

sched = BlockingScheduler()
sched.add_job(job_function, 'interval', seconds=30)
sched.start()

