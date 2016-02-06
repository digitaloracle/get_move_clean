from deluge_api import *
from plex_scanner import refresh_plex
from cleaner import *
import time
import psutil
import math
import sys


logging.basicConfig(filename='move_claen.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def cpu_load(samples=4):
    cpu_stats = list()
    for sample in xrange(samples):
        cpu_stats.append(psutil.cpu_percent())
        time.sleep(3)
    return math.floor(math.fsum(cpu_stats)/len(cpu_stats))


def run_routines():
    try:
        for tor in remove_completed():
            logging.info('removed %s from deluge' % tor)
    except TypeError as te:
        logging.info('no deluge torrents to clean')
        pass
    time.sleep(5)
    sys.stderr.write('\ninitiated cleaner')
    if clean():
        sys.stderr.write('\ninitiated plex rescan')
        refresh_plex()

if __name__ == '__main__':
    try:
        minute = 60
        while 1:
            if cpu_load() < 30:
                run_routines()
                time.sleep(minute*30)
            else:
                logging.info("cpu avarage was above 30%, waiting 30 minutes")
                time.sleep(minute*5)
    except KeyboardInterrupt:
        sys.stderr.write("\nDone")
        sys.exit(0)
