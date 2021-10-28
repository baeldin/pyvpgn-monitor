import datetime as dt
import psutil
import subprocess
import logging


# exectuable paths
exec_path = {
    "PvPGN": "C:/pvpgn/release/PvPGN.exe",
    "D2DBS": "C:/pvpgn/release/D2DBS.exe",
    "D2CS": "C:/pvpgn/release/D2CS.exe",
    "D2GS": "C:/pvpgn/d2gs/D2GS.exe"
}
# working directories for executables
cwd = {
    "PvPGN": "C:/pvpgn/release/",
    "D2DBS": "C:/pvpgn/release/",
    "D2CS": "C:/pvpgn/release/",
    "D2GS": "C:/pvpgn/d2gs/"
}


def get_process_details(p):
    start_date = dt.datetime(1970, 1, 1) + dt.timedelta(seconds=p.create_time())
    running = dt.datetime.utcnow() - start_date
    pid = p.pid
    logging.debug("{:s} has PID {:d} and has been running for {:d} seconds".format(
        p.name(), pid, int(running.total_seconds())))
    return True


def check_processes():
    # running_dict = {"D2GS": False, "PvPGN": False, "D2CS": False, "D2DBS": False}
    running_dict = {"D2GS": False}
    for p in psutil.process_iter():
        for process in running_dict.keys():
            if process in p.name():
                running_dict[process] = get_process_details(p)
    return running_dict


def restart_missing(running_dict):
    for process, status in running_dict.items():
        if not status:
            logging.info(process+" is not running, restarting it now...")
            subprocess.Popen(exec_path[process], cwd=cwd[process])
