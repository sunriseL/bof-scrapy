import time
import requests
from lxml import etree
import deploy
import os
dir = "data"

class Get:
    def __init__(self,event_num=123,event_title="BOFXV"):
        self.event_num = event_num
        self.event_title = event_title
        self.url_pattern = "http://manbow.nothing.sh/event/event.cgi?action={0}&num={1}&event={2}"
        self.action = "sp"
    def getList(self):
        self.action = "sp"
        date = time.strftime("%m/%d %H:00", time.localtime())
        file = time.strftime("%m-%d-%H", time.localtime())
        response = requests.get(self.url_pattern.format(self.action,0,self.event_num))
        response.encoding = 's_jisx0213'
        html = etree.HTML(response.text,etree.HTMLParser())
        headers = html.xpath('//table/thead/*/th/text()')
        dataxmls = html.xpath('//table/tbody/tr')
        #print(headers)
        datas = []
        for data in dataxmls:
            datas.append(data.xpath('td//text()').append(date))
        deploy.deploy(headers,datas,os.path.join(dir,self.event_title + "-" + file + ".csv"))
#Get().getList()