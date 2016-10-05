import RPi.GPIO as G
import time
import os
import signal
import sys

import logging
import logging.handlers

#print 'In?'
#print G.input(14)

flag = '/opt/cyrkulacja/run/pompuj'
logfile = '/opt/cyrkulacja/log/cyrkulacja.log'

log = logging.getLogger('cyrkulacja')
log.setLevel(logging.DEBUG)
rfh = logging.handlers.RotatingFileHandler(logfile, maxBytes=1024000, backupCount=5)
fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
rfh.setFormatter(fmt)
log.addHandler(rfh)

def configure_pins():
    G.setmode(G.BCM)
    G.setup(14, G.OUT)

def get_sleep_interval(file=None):
    interval=0
    with open(file, 'r') as f:
        interval = f.readline()
    interval = int(interval.strip()) #throws ValueError
    return interval

def turn_on():
    G.output(14, G.LOW)

def turn_off():
    G.output(14, G.HIGH)

def sigterm_handler(signal, frame):
    G.cleanup()
    log.info('SIGTERM received - exiting')
    sys.exit(0)

if __name__ == '__main__':
    log.info('Master daemon starting')
    signal.signal(signal.SIGTERM, sigterm_handler)
#    signal.signal(signal.SIGINT, sigterm_handler)
    
    configure_pins()
    log.info('Pins configured')
    while True:
        try:
            flag_present = os.path.isfile(flag)
            if flag_present:
                log.info('Flag present')
                how_long = get_sleep_interval(file=flag)
                log.info('Turning on for: ' + str(how_long) + ' seconds')
                turn_on()
                os.remove(flag)
                time.sleep(how_long)
                turn_off()
                log.info('Finished')
            else:
                time.sleep(10)
        except ValueError:
            os.remove(flag)
            log.warning('Bad flag value supplied - removing')
        except KeyboardInterrupt:
            log.warning('KeyboardInterrupt')
            G.cleanup()
            sys.exit(0)
        except:
            G.cleanup()
            log.critical(sys.exc_info()[0])
            log.info('Stopped after exception')
            sys.exit(0)
