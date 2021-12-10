import telnetlib
import time
import process_monitor
import psutil


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
        self.passwd = b"Tsuru110ESR\n"
        self.timeout = 100


    def telnet(self):
        """ open and return telnet session """
        session = telnetlib.Telnet(self.host, self.port, self.timeout)
        time.sleep(2)
        session.write(self.passwd)
        time.sleep(2)
        return session


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
        session = self.telnet()
        restart_command = "restart "+str(delay)+"\n"
        restart_command_bytes = bytes(restart_command, 'utf-8')
        session.write(restart_command_bytes)
        session.write(b"exit")
        if kill:
            self.kill(delay)


    def kill(self, delay):
        """ Kill the process of D2GS after [delay] seconds."""
        time.sleep(delay)
        process_dict = process_monitor.check_processes()
        d2gs_id = process_dict['D2GS']
        p = psutil.Process(d2gs_id)
        p.terminate()


    def msg(self, msg):
        with self.telnet() as session:
            msg_command = "msg sys #all \""+msg+"\"\n"
            msg_command_bytes = bytes(msg_command, 'utf-8')
            session.write(msg_command_bytes)
            session.write(b"exit")


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
        with self.telnet() as session:
            # session.read_all()
            session.read_until(b"Password:")
            session.write(b"status\n")
            time.sleep(1)
            session.write(b"exit\n")
            time.sleep(1)
            #session.read_until(b"D2GS> status")
            status_str = session.read_all().decode('ascii')
        return status_str
    
