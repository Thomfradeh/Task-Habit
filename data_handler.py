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


if __name__ == '__main__':
    print(fetch_daily_tasks())
    print(fetch_lastweek())
