import argparse
import d2gs
import time


def parsing_arguments():
    parser = argparse.ArgumentParser(description='Restart D2GS in N seconds')
    parser.add_argument('-N', '--delay', type=int, default=902)
    args = parser.parse_args()
    return args


def wait_before_restart(gs, wait_time):
    """ If the delay is more than 2 minutes, warn players using
    messages via telnet, so they can still create and join games
    up until 120 seconds before the restart """
    wait_time_minutes = int(float(wait_time)/60.)
    wait_time_residual = wait_time - wait_time_minutes*60
    wait_time_rounded = 60*wait_time_minutes
    time.sleep(wait_time - wait_time_rounded)
    while wait_time_rounded > 120:
        gs.msg("This server will be restarted in {:d} minutes.".format(int(wait_time_rounded/60)))
        wait_time_rounded -= 60
        time.sleep(60)


def main():
    args = parsing_arguments()
    gs = d2gs.D2GS('localhost', 8888)
    wait_before_restart(gs, args.delay)
    gs.restart(kill=True, delay=122)


if __name__ == "__main__":
    main()
