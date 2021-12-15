import os
import logging
import subprocess
import psutil


logging.basicConfig(filename='/home/d2esr/char_backup/backup.log', encoding='utf-8', level=logging.DEBUG)
# process names and full paths
dir_dict = {
    'bnetd': '/home/d2esr/pvpgn/sbin',
    'd2cs': '/home/d2esr/pvpgn/sbin',
    'd2dbs': '/home/d2esr/pvpgn/sbin',
    'D2GS': '/home/d2esr/d2gs'
    }
bin_dict = {
    'bnetd': '/home/d2esr/pvpgn/sbin/bnetd',
    'd2cs': '/home/d2esr/pvpgn/sbin/d2cs',
    'd2dbs': '/home/d2esr/pvpgn/sbin/d2dbs',
    'D2GS': 'wine ./D2GS.exe'
    }


def get_PIDs(process_name=None):
    '''
    Arguments:
    str    process_name      explicitly search for process with given string
    Returns:
    dict   pids              contains all checke process names and their pid
                             contains None for missing processes
    bool   missing           False if all processes are running, True if at least
                             one is missing
    '''
    missing = False
    if process_name:
        processes = [process_name]
    else:
        processes = ['bnetd', 'd2cs', 'd2dbs', 'D2GS']
    pids = {}
    for process_name in processes:
        running = False
        for proc in psutil.process_iter():
            if process_name.lower() in proc.name().lower():
                print("found "+process_name+" found with pid "+str(proc.pid))
                pids[process_name] = proc.pid
                running = True
        if not running:
            pids[process_name] = None
            missing = True
    return(pids, missing)


def restart_proc(pids):
    '''
    Function loops over dictionary with process names and pids
    provided by get_PIDs() and restarts any process that was not
    found.
    Arguments:
    dict   pids             contains all process names and pids
    Returns:
    None
    '''
    for proc, pid in pids.items():
        if not pid:
            rerun_pids = True
            logging.info("launching "+proc)
            shell = True if proc == 'D2GS' else False
            print("Restarting "+proc)
            stuff = subprocess.Popen(bin_dict[proc], cwd=dir_dict[proc], shell=shell)


def write_pids(pids):
    with open('/home/d2esr/pvpgn_pids', 'w+') as f:
        for key, item in pids.items():
            f.write(str(key) + " " + str(item) + "\n")
    logging.info("wrote PIDs to /home/d2esr/pvpgn_pids")


def read_pids():
    pids = {}
    with open('/home/d2esr/pvpgn_pids', 'r') as f:
        for line in f:
            (key, val) = line.split()
            pids[str(key)] = int(val)
    print(pids)

def main():
    pids, missing_pid = get_PIDs()
    if missing_pid:
        restart_proc(pids)
    print(pids)
    write_pids(pids)




if __name__ == "__main__":
    main()

