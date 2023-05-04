import telnetlib
import time
import datetime as dt
import process_monitor
import psutil
import pandas as pd
import os


# positions of values in returns from d2gs when checking games and chars via telnet
cut = {
        'games': [5, 17, 17, 6, 9, 6, 12, 11, 6, 10, 3],
        'chars': [5, 17, 17, 17, 7, 7, 10]
}
columns = {
        'games': ['No.', 'GameName', 'GamePass', 'ID', 'GameVer', 'Type', 'Difficulty', 'Ladder', 'Users', 'CreateTime', 'Dis'],
        'chars': ['No.', 'AcctName', 'CharName', 'IPAddress', 'Class', 'Level', 'EnterTime']
}
dtypes = {
        'games': [int, str, str, int, str, str, str, str, int, str, str],
        'chars': [int, str, str, str, str, int, str]
}

with open("passwd") as f:
    telnet_passwd = bytes(f.read(), "utf-8")

run_command = "docker run -it -v /home/d2esr/d2gs:/D2GS/drive_c/Diablo2 --ip 172.17.0.2 -p 4000:4000 thomasesr/d2gs:latest &"

class D2GS():
    """ D2GS Class
    Fetch info from a running Diablo 2 Game Server using telnet
    Parameters:
    str host ......... hostname
    int port ......... port

    Password needs to be set here for the moment. This is assumed to run on the
    same machine."""
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.passwd = telnet_passwd
        self.timeout = 100
        self.dockerID = self.get_container_ID()
        self.session = self.telnet()


    def get_container_ID(self):
        os.system('docker container ls | tail -n 1 | cut -f 1 -d " " > d2gs_docker_container_ID')
        with open("d2gs_docker_container_ID") as f:
            dockerID = f.read()
        return dockerID
        

    def telnet(self):
        """ open and return telnet session """
        session = telnetlib.Telnet(self.host, self.port, self.timeout)
        time.sleep(5)
        session.write(self.passwd)
        time.sleep(2)
        return session


    def telnet_command(self, cmd):
        if not cmd[-1] == "\n":
            cmd+="\n"
        cmd_bytes = bytes(cmd, 'utf-8')
        self.session.read_very_eager()
        self.session.write(cmd_bytes)
        time.sleep(0.5)
        return self.session.read_very_eager().decode().split("\r\n")


    def restart(self, kill=True, delay=902):
        """ open telnet and initiate a restart
        Parameters:
        bool kill ........ Kill process after restarting server?
        int delay ........ delay in seconds

        Initiate a restart of the game server. The kill parameter determines whether
        the actual process will be killed after the delay has run out. This is used
        to force restart the process and prevent memory iusses, ideal for scheduled
        restarts of the game server. The server is restarted after [delay] seconds.

        Using telnet first, then killing the process assures that the players get a
        countdown warning and all memory is cleaned up."""
        restart_command = "restart "+str(delay)+"\n"
        restart_command_bytes = bytes(restart_command, 'utf-8')
        self.session.write(restart_command_bytes)
        self.session.write(b"exit")
        time.sleep(delay)
        os.system("docker container restart {:s}".format(self.dockerID))


    def kill(self, delay):
        """ Kill the process of D2GS after [delay] seconds."""
        time.sleep(delay)
        process_dict = process_monitor.check_processes()
        d2gs_id = process_dict['D2GS']
        p = psutil.Process(d2gs_id)
        p.terminate()


    def msg(self, msg):
        msg_command = "msg sys #all \""+msg+"\"\n"
        msg_command_bytes = bytes(msg_command, 'utf-8')
        self.session.write(msg_command_bytes)
        self.session.write(b"exit")


    def status(self):
        """ use status_raw() to obtain raw telnet output and then extract some info
        from the string by splitting it and generating a usable dictionary."""
        status_str = self.status_raw()
        status_lines = [i.replace("\n","").split(":") for i in status_str.split("\r")]
        status_dict = {}
        for lin in status_lines:
            if "Setting maximum game" in lin[0]:
                status_dict['maxgames_set'] = int(lin[1].replace(" ","")) 
            if "Current maximum game" in lin[0]:
                status_dict['maxgames_cur'] = int(lin[1].replace(" ","")) 
            if "Current running game" in lin[0]:
                status_dict['ngames'] = int(lin[1].replace(" ","")) 
            if "Current users in game" in lin[0]:
                status_dict['nusers'] = int(lin[1].replace(" ","")) 
            if "Maximum prefer users" in lin[0]:
                status_dict['max_users'] = int(lin[1].replace(" ","")) 
            if "Maximum game life" in lin[0]:
                status_dict['max_game_life'] = int(lin[1].replace(" ","").replace("seconds","")) 
        return status_dict
            
    def status_raw(self):
        """ open telnet session and send the 'status' command, then return its result as string."""
        # session.read_very_eager()
        self.session.read_until(b"Password:")
        self.session.write(b"status\n")
        time.sleep(1)
        self.session.write(b"exit\n")
        time.sleep(1)
        #session.read_until(b"D2GS> status")
        status_str = self.session.read_very_eager().decode('ascii')
        return status_str
    

    def games(self):
        time.sleep(2)
        gl = self.telnet_command("gl\n")
        games, columns = self.split_return(gl, 'games')
        return pd.DataFrame(games, columns = columns)


    def chars_in_game(self, game_id):
        time.sleep(2)
        cl = self.telnet_command("cl "+str(game_id)+"\n")
        chars, columns = self.split_return(cl, 'chars')
        return pd.DataFrame(chars, columns = columns)

    def we(self):
        #         [['we'],
        #  ['     World Event', 'Enable'],
        #  ['        Key Item', "Devil's Food"],
        #  ['     Total Spawn', '21'],
        #  ['      Base Count', '17'],
        #  ['Last Spawn Count', '87'],
        #  ['   Current Count', '87'],
        #  ['Next Spawn Count', '104'],
        #  ['  Last Sell Time', '2021-12-10 15:32:56'],
        #  [' Last Spawn Time', '2021-12-10 15:32:56'],
        #  [''],
        #  ['D2GS> ']]
        we_list = self.telnet_command("we")
        we_out = {}
        for we_entry_ in we_list:
            we_entry = we_entry_.split(" : ")
            if type(we_entry) == list and len(we_entry) == 2:
                print(we_entry)
                if not 'Time' in we_entry[0]:
                    we_out[we_entry[0].replace(" ","")] = we_entry[1]
                else:
                    we_out[we_entry[0].replace(" ","")] = dt.datetime.strptime(we_entry[1], "%Y-%m-%d %H:%M:%S")
        return we_out


    def split_return(self, in_list, mode):
        line_identifiers = {'games': "GameName", 'chars': "AcctName"}
        keep = False
        list_entries = []
        for in_line in in_list:
            if keep:
                if "-----" in in_line:
                    keep = False
                    continue
                list_entry_ = list(chunkstring(in_line[2:-4], cut[mode]))
                list_entry = []
                for g, dtype in zip(list_entry_, dtypes[mode]):
                    list_entry.append(dtype(g))
                list_entries.append(list_entry)
            if line_identifiers[mode] in in_line:
                columns = multi_space_to_one(in_line[2:-2].replace("-"," ")).split(" ")
                keep = True
        return list_entries, columns

def multi_space_to_one(s):
    """
    replace multiple spaces in string with single string
    """
    m = 0
    n = 1
    while n - m > 0:
        n = len(s)
        s = s.replace("  ", " ")
        m = len(s)
    return s


def cut_trailing_spaces(s):
    """
    cut trailing spaces from end of string
    """
    while True:
        if s[-1] == " ":
            s = s[0:-1]
        else:
            return s


def chunkstring(string, lengths):
    return (string[pos:pos+length].strip()
            for idx,length in enumerate(lengths)
            for pos in [sum(map(int, lengths[:idx]))])


