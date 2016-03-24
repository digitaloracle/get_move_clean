from deluge_api import *
from plex_scanner import refresh_plex
from cleaner import *
import time
import psutil
import math
import sys
import logging


logging.basicConfig(filename='move_claen.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')


def cpu_load(samples=4):
    cpu_stats = list()
    for sample in xrange(samples):
        cpu_stats.append(psutil.cpu_percent())
        time.sleep(3)
    return math.floor(math.fsum(cpu_stats)/len(cpu_stats))


def run_routines():
    comp = remove_completed()
    if len(comp) > 0:
        for tor in comp:
            logging.info('removed %s from deluge' % tor)
        if clean():
            logging.info('cleaner done')
            logging.info('initiated plex rescan')
            refresh_plex()
        else:
            logging.debug('nothing to move')
    else:
        logging.info('no deluge torrents to clean')

if __name__ == '__main__':
    try:
        minute = 60
        while 1:
            if cpu_load() < 30:
                run_routines()
                sys.stderr.write('\n%s: sleeping for 10 minutes' % time.ctime())
                time.sleep(minute*10)
            else:
                logging.info("cpu avarage was above 30%, waiting 5 minutes")
                time.sleep(minute*5)
                sys.stderr.write('\n%s: sleeping for 5 minutes' % time.ctime())
    except KeyboardInterrupt:
        sys.stderr.write("\nDone")
        sys.exit(0)
