
import csv
import os
import deploy
data_header = ['No.', 'Team', 'Artist', 'Genre', 'Title', 'Impr', 'Total', 'Median', 'Regist', 'Update']
target_type = ['name','type','value','date']

def turn_data_into_target(data,date):
    result = []
    result.append(data[data_header.index("Title")])
    result.append(data[data_header.index("Artist")])
    result.append(data[data_header.index("Total")])
    result.append(date)
    return result

def compact(Event="BOFXV"):
    print("Compacting {0}...".format(Event))
    names = []
    datas = []
    for dirpath,dirnames,filenames in os.walk('data'):
    	if dirpath.startswith('data'):
		    for fn in filenames:
			    if fn.startswith(Event):
				    names.append(fn)
    names.sort()
    for name in names:
        times = name[:name.index(".")].split("-")[-3:]
        date = "{0}/{1} {2}:00".format(times[0],times[1],times[2])
        print(date)
        with open(os.path.join(dirpath,name),encoding="utf-8") as f:
            r = csv.reader(f)
            for index,row in enumerate(r):
                if index > 0:
                    datas.append(turn_data_into_target(row,date))
    deploy.deploy(target_type,datas)
    print("Compact Over")
#compact()
