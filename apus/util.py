import datetime
import os

import psutil


def gprint(s: str):
    time = datetime.datetime.now()
    print(f'[{time.hour}:{time.minute}:{time.second}] {s}')


def truncate(f):
    return "{0:.2f}".format(f)


def get_hardware_info():
    proc = psutil.Process(os.getpid())
    cpu = truncate(proc.cpu_times().user)
    rss = truncate(proc.memory_info().rss / 1024 / 1024)  # MB
    vms = truncate(proc.memory_info().vms / 1024 / 1024)
    thread = proc.num_threads()
    i = truncate(proc.io_counters().read_bytes / 1024 / 1024)  # MB
    o = truncate(proc.io_counters().write_bytes / 1024)  # MB
    return f'CPU: **{cpu}%**\nRAM: **Physical: {rss}MB, Virtual: {vms}MB**\nThreads: **{thread}**\nI/O: **{i}/{o}MB**'
