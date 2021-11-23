import telnetlib
import time
import argparse
import process_monitor
import psutil

host = 'localhost'
port = 8888
timeout = 100


parser = argparse.ArgumentParser(description='Restart D2GS in N seconds')
parser.add_argument('-N', '--delay', type=int, default=900)
args = parser.parse_args()


def kill_process(delay):
    time.sleep(delay)
    process_dict = process_monitor.check_processes()
    d2gs_id = process_dict['D2GS']
    print(process_dict)
    p = psutil.Process(d2gs_id)
    print(p)
    p.terminate()



with telnetlib.Telnet(host, port, timeout) as session:
    time.sleep(2)
    session.write(b"Tsuru110ESR\n")
    time.sleep(2)
    delay = args.delay+2
    restart_command = "restart "+str(delay)+"\n"
    restart_command_bytes = bytes(restart_command, 'utf-8')
    session.write(restart_command_bytes)
    session.write(b"exit")
    kill_process(delay)
