import argparse
import d2gs
import time
import numpy as np


def parsing_arguments():
    parser = argparse.ArgumentParser(description='Restart D2GS in N seconds')
    parser.add_argument('-N', '--delay', type=int, default=902)
    args = parser.parse_args()
    return args


def int_seconds_to_string(s):
    minutes = int(np.floor(s/60.))
    seconds = int(s - 60 * minutes)
    return "{:02d}:{:02d}".format(minutes, seconds)

def wait_before_restart(gs, wait_time):
    """ If the delay is more than 2 minutes, warn players using
    messages via telnet, so they can still create and join games
    up until 120 seconds before the restart """
    print("Restart in {:d} seconds requested.".format(wait_time))
    wait_time_minutes = int(float(wait_time)/60.)
    wait_time_residual = wait_time - wait_time_minutes*60
    wait_time_rounded = 60*wait_time_minutes
    print("Restart script will sleep for {:d} seconds before first message to server.".format(wait_time - wait_time_rounded))
    time.sleep(wait_time - wait_time_rounded)
    while wait_time_rounded > 1:
        delta_t = 60 if wait_time_rounded > 120 else 15
        print("opening D2GS telnet session for message...")
        print("Sending restart message (timer={:s})".format(
            int_seconds_to_string(wait_time_rounded)))
        gs = d2gs.D2GS('172.17.0.2', 8888)
        gs.msg("This game server will be restarted in {:s}.".format(
            int_seconds_to_string(wait_time_rounded)))
        gs.session.close()
        wait_time_rounded -= delta_t
        time.sleep(delta_t)


def main():
    args = parsing_arguments()
    print("opening D2GS telnet session...")
    gs = d2gs.D2GS('172.17.0.2', 8888)
    print("Starting restart wait now")
    wait_before_restart(gs, args.delay)
    gs.restart(kill=True, delay=2)


if __name__ == "__main__":
    main()
