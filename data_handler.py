import csv
from datetime import date, timedelta


def fetch_daily_tasks():
    with open('dailytask.csv', 'r') as rawdailytasks:
        rawdata = csv.reader(rawdailytasks)
        datalist = list(rawdata)

    return datalist[1:]


def fetch_lastweek():
    lastweekdates = []
    for c in range(6, 0, -1):
        lastweekdates.append((date.today() - timedelta(days=c)).isoformat())

    lastweekdays = []
    for c in range(1, 8):
        weekday = (date.today().weekday()-c) % 7
        lastweekdays.append(weekday)

    return lastweekdates, lastweekdays


def recreate_dailytasks(task_list):
    with open('dailytask.csv', 'w') as newtaskscsv:
        headers = 'name,description,recurrence,date_list\n'
        newtaskscsv.write(headers)

        for task in task_list:
            current_date = date.isoformat(date.today())
            if task[4] == 1 and current_date not in task[3]:
                task[3] += ';' + current_date
            elif task[4] == 0 and current_date in task[3]:
                task[3] = task[3][:-11]
            task.pop(4)

            task_line = f'{task[0]}'
            for x in task[1:]:
                task_line += ',' + x
            newtaskscsv.write(task_line+'\n')


if __name__ == '__main__':
    print(fetch_daily_tasks())
    print(fetch_lastweek())
