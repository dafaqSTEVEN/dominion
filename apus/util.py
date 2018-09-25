import datetime


def gprint(s: str):
    time = datetime.datetime.now()
    print(f'[{time.hour}:{time.minute}:{time.second}] {s}')
