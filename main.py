import datetime as dt
import threading
import math
import time
import os
import process_monitor
import pvpgn_backup
import logging


str_now = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
logfile_name = 'C:/pyvpgn_{:s}.log'.format(str_now)
logging.basicConfig(
    filename=logfile_name,
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')


def get_next_d2gs_restart_time():
    """
    returns dt.datetime object with:
    4 UTC of the current day if it is before 4 AM
    4 UTC of the next day if it is after 3 AM
    """
    if dt.datetime.now().hour <= 4:
        next_3am = dt.datetime.combine(
            dt.date.today(),
            dt.time())+dt.timedelta(hours=4)
    else:
        next_3am = dt.datetime.combine(
            dt.date.today(),
            dt.time())+dt.timedelta(hours=28)
    seconds_until_3am = (next_3am - dt.datetime(1970, 1, 1)).total_seconds()
    return seconds_until_3am


def get_next_backup_time():
    year, month, day, hour, minute, _, _, _, _ = tuple(dt.datetime.now().timetuple())
    minute = int(math.ceil(minute + 1))  # add one minute to avoid instant backup
    next_backup = dt.datetime(year, month, day, hour, minute)
    seconds_until_next_backup = (next_backup - dt.datetime(1970, 1, 1)).total_seconds()
    return seconds_until_next_backup


next_process_check_call = time.time()
next_d2gs_restart = get_next_d2gs_restart_time()
skip_next_d2gs_restart = True
next_backup_tick = get_next_backup_time()


def process_check_ticker():
    global next_process_check_call
    running_dict = process_monitor.check_processes()
    process_monitor.restart_missing(running_dict)
    next_process_check_call += 10
    threading.Timer(next_process_check_call - time.time(), process_check_ticker).start()


def d2gs_restart_ticker():
    global next_d2gs_restart
    global skip_next_d2gs_restart
    if skip_next_d2gs_restart:
        skip_next_d2gs_restart = False
    else:
        logging.info("Killing and restarting d2gs now")
        os.system("taskkill /F /im D2GS.exe")
    next_d2gs_restart += 86400
    threading.Timer(next_d2gs_restart - time.time(), d2gs_restart_ticker).start()


def pvpgn_backup_ticker():
    global next_backup_tick
    backup_archive_name = pvpgn_backup.backup()
    logging.info("Backed up pvpgn files to "+backup_archive_name)
    next_backup_tick += 600
    logging.info("archive, next backup will take place in 10 minutes")
    threading.Timer(next_backup_tick - time.time(), pvpgn_backup_ticker).start()


def main():
    threading.Thread(process_check_ticker())
    threading.Thread(d2gs_restart_ticker())
    threading.Thread(pvpgn_backup_ticker())


if __name__ == "__main__":
    main()
