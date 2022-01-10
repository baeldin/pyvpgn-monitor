import os
import logging
import subprocess
import psutil
import datetime as dt

user = 'firesnake'

logging.basicConfig(
        filename='srv.log', 
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        encoding='utf-8', 
        level=logging.DEBUG)

# process names and full paths
dir_dict = {
    'bnetd': '/home/' + user + '/pvpgn/sbin',
    'd2cs': '/home/' + user + '/pvpgn/sbin',
    'd2dbs': '/home/' + user + '/pvpgn/sbin',
    'D2GS': '/home/' + user + '/d2gs'
    # 'D2GSSVC': '/home/' + user + '/d2gs'
    }
bin_dict = {
    'bnetd': '/home/' + user + '/pvpgn/sbin/bnetd',
    'd2cs': '/home/' + user + '/pvpgn/sbin/d2cs',
    'd2dbs': '/home/' + user + '/pvpgn/sbin/d2dbs',
    'D2GS': '/usr/local/bin/wine /home/' + user + '/d2gs/D2GS.exe',
    #'D2GSSVC': 'wine net start D2GS'
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
        # processes = ['bnetd', 'd2cs', 'd2dbs', 'D2GSSVC']
        processes = ['bnetd', 'd2cs', 'd2dbs', 'D2GS']
    pids = {}
    for process_name in processes:
        running = False
        for proc in psutil.process_iter():
            if process_name.lower() in proc.name().lower():
                logging.info("found "+process_name+" found with pid "+str(proc.pid))
                pids[process_name] = proc.pid
                running = True
        if not running:
            logging.debug("Did not find "+process_name)
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
            # D2GS is handled by the service!
            logging.debug(bin_dict[proc])
            logging.debug(dir_dict[proc])
            logging.debug(shell)
            stuff = subprocess.Popen(bin_dict[proc], cwd=dir_dict[proc], shell=shell)


def write_pids(pids):
    with open('/home/' + user + '/pvpgn_pids', 'w+') as f:
        for key, item in pids.items():
            f.write(str(key) + " " + str(item) + "\n")
    # logging.info("wrote PIDs to /home/" + user + "/pvpgn_pids")


def read_pids():
    pids = {}
    with open('/home/' + user + '/pvpgn_pids', 'r') as f:
        for line in f:
            (key, val) = line.split()
            pids[str(key)] = int(val)
    logging.info(repr(pids))

def main():
    pids, missing_pid = get_PIDs()
    if missing_pid:
        restart_proc(pids)
    # print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")+repr(pids))
    write_pids(pids)




if __name__ == "__main__":
    main()

