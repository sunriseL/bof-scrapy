import get
import deploy
import compact
import schedule
import time

get_schedule = ['09:05','12:05','15:05','18:05','21:05']
every_hour_schedule = ["{:0>2d}:05".format(i) for i in range(24)]
get_schedule = every_hour_schedule
event_num = 127
event_title = "BOFXV"
def getTask():
    getHandler = get.Get(event_num=event_num,event_title=event_title)
    while True:
        try:
            getHandler.getList()
            compact.compact(event_title)
            break
        except:
            pass


def main():
    compact.compact()
    #print(every_hour_schedule)
    for sche in get_schedule:
        schedule.every().day.at(sche).do(getTask)

    while True:
        schedule.run_pending()
        time.sleep(60)
	

    

if __name__ == "__main__":
    main()
