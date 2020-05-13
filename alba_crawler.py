import requests
import os
import telegram
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

bot = telegram.Bot(token='token')
chat_id = chat_id

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def job_function():
    html = requests.get('http://042.albamon.com/list/gi/mon_duty_list.asp?ps=50&ob=0&lvtype=1&rArea=,G000,&sDutyTerm=,5,10,20&rWDate=1&Empmnt_Type=')
    html.encoding = 'euc-kr'
    soup = BeautifulSoup(html.text, 'html.parser')
    posts = soup.select('p.cTit > a')
    link = posts[0].get('href')
    latest = posts[0].text
    
    with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+') as f_read:
        before = f_read.readline()
        f_read.close()
        if before != latest:
            bot.sendMessage(chat_id=chat_id,text='<단기알바알림!> '+latest+'\n▽ 지원하러가기'+'\nhttp://042.albamon.com'+link)
            with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write:
                f_write.write(latest)
                f_write.close()

sched = BlockingScheduler()
sched.add_job(job_function, 'interval', seconds=30)
sched.start()

