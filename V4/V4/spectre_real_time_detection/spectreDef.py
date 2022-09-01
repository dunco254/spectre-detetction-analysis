from multiprocessing import Process, Pipe
from pypapi import events
import psutil
import os
import proc_events
from bcolors import bcolors
from netlink_process_monitor import NetlinkProcessMonitor as ProcessMonitor
from watcher import Watcher
from detector import Detector
from datetime import datetime 


def on_process_start(pid):
    obj = datetime.now()
    watcher_send_conn.send((proc_events.PROC_START, pid))
    print(f"{bcolors.OKGREEN}Start Process at {obj.hour}:{obj.minute}:{obj.second}:{obj.microsecond} {pid}")


def on_process_end(pid):
    obj = datetime.now()
    watcher_send_conn.send((proc_events.PROC_END, pid))
    print(f"{bcolors.WARNING}End Process at {obj.hour}:{obj.minute}:{obj.second}:{obj.microsecond} {pid}")


if __name__ == '__main__':
    events = [events.PAPI_TOT_INS, events.PAPI_L3_TCM, events.PAPI_L3_TCA]

    watcher_recv_conn, watcher_send_conn = Pipe(False)
    detector_recv_conn, detector_send_conn = Pipe(False)
    watcher = Watcher(events, 0.1, watcher_recv_conn, detector_send_conn)
    detector = Detector(detector_recv_conn, None)
    whitelist = []
    own_pid = os.getpid()
    whitelist.append(own_pid)
    running_pids = [x for x in psutil.pids() if x not in whitelist]
    p = Process(target=watcher.start, args=(running_pids,))
    p.start()
    p2 = Process(target=detector.start)
    p2.start()

    process_monitor = ProcessMonitor()
    process_monitor.on_process_start.append(on_process_start)
    process_monitor.on_process_end.append(on_process_end)

    process_monitor.start()
