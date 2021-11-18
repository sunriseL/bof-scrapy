
import csv
import os
import deploy
import functools
data_header = ['No.', 'Team', 'Artist', 'Genre', 'Title', 'Impr', 'Total', 'Median', 'Regist', 'Update']
target_type = ['name','type','value','date']

def turn_data_into_target(data,date):
    result = []
    result.append(data[data_header.index("Title")])
    result.append(data[data_header.index("Artist")])
    result.append(data[data_header.index("Total")])
    result.append(date)
    return result

def bofxvi_compare(x,y):
    x = x[7:-4]
    y = y[7:-4]
    m_x = x[0:2]
    m_y = y[0:2]
    if m_x == "01": m_x = "13"
    if m_y == "01": m_y = "13"

    d_x = x[3:5]
    d_y = y[3:5]
    h_x = x[6:8]
    h_y = y[6:8]
    if m_x > m_y: return 1
    elif m_x < m_y: return -1

    if d_x > d_y: return 1
    elif d_x < d_y: return -1

    if h_x > h_y: return 1
    elif h_x < h_y: return -1

    return 0


def filter_log_list(dirpath, names):
    new_names = []
    datas = []
    for index, name in enumerate(names):
        with open(os.path.join(dirpath,name),encoding="utf-8") as f:
            time_slice = name[7:-4]
            # end = time_slice == "12-20-23"
            # final_end = time_slice == "01-05-20"
            # last = (time_slice > "12-20-23" or time_slice.startswith("01")) and not final_end
            r = csv.reader(f)
            header = next(r)
            rows = [row for row in r]
            rows.sort(key=lambda row: eval(row[data_header.index("Total")]),reverse=True)
            rows = rows[:20]
            datas.append(rows)

            ''' skip log which does not have data '''
            if eval(rows[0][data_header.index("Total")]) == 0:
                continue

            '''  '''
            if index != 0:
                titles = [row[data_header.index("Title")] for row in rows]
                prev_titles = [row[data_header.index("Title")] for row in datas[index-1]]
                s = 0
                for prev_row, row in zip(datas[index-1], rows):
                    s += eval(row[data_header.index("Total")]) - eval(prev_row[data_header.index("Total")])
                # if (s > 8000 or s < -8000 or end or final_end) and not last:
                if s > 8000 or s < -8000:
                    print(time_slice)
                    new_names.append(name)
            else:
                new_names.append(name)
            #print(titles)
    return new_names

def compact(Event="BOFXV"):
    print("Compacting {0}...".format(Event))
    names = []
    datas = []
    for dirpath,dirnames,filenames in os.walk('data'):
    	if dirpath.startswith('data'):
		    for fn in filenames:
			    if fn.startswith(Event):
				    names.append(fn)
    dirpath = 'data'
    names.sort(key=functools.cmp_to_key(bofxvi_compare))
    names = filter_log_list(dirpath, names)
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

def compact_with_list(names):
    names.sort(key=functools.cmp_to_key(bofxvi_compare))
    datas = []
    dirpath="data"
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
#compact()
