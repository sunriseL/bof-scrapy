#coding:utf-8#
import csv
path = "/home/sunrise/static/data.csv"
#path="data.csv"

data_header = ['No.', 'Team', 'Artist', 'Genre', 'Title', 'Impr', 'Total', 'Median', 'Regist', 'Update']
target_type = ['name','type','value','date']

def deploy(headers,datas,path=path):
    f = open(path,"w",newline="",encoding="utf-8")
    w = csv.writer(f)
    w.writerow(headers)
    w.writerows(datas)
#deploy(["1","2"],[["aa","aa"],["bb","bb"]])