import signal
import logging
import time
import os
import sys
import glob
from itertools import islice


exit_flag = False
start_time = time.time()
logging.basicConfig(filename='log.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped
    here as well (SIGHUP?.Basically it just sets a global flag, and main()
    will exit it's loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    signames = dict((k, v) for v, k in reversed(sorted(
        signal.__dict__.items())) if v.startswith('SIG')
        and not v.startswith('SIG_'))
    logging.warning('Received {} signal.'.format(signames[sig_num]))
    logging.debug('Program has stopped.')
    logging.debug('Program was up for about ' +
                  str(int(time.time() - start_time)) + ' seconds.')
    global exit_flag
    exit_flag = True
    logging.info(exit_flag)


def main(args):
    src_dir = args[0]
    magic_text = args[1]
    polling_interval = float(args[2])
    file_extn = args[3]
    # Hook these two signals from the OS ..
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.
    if exit_flag:
        logging.info(exit_flag)
    if not exit_flag:
        logging.debug('Program has started.')
    file_dict = {}
    while not exit_flag:
        # Do my long-running stuff
        if os.path.isdir(src_dir):
            path = src_dir+'*'+file_extn
            files = glob.glob(path)
            for name in files:
                try:
                    with open(name) as f:
                        if name in file_dict.keys():
                            check_from_line = file_dict[name] + 1
                            skipped = islice(f, check_from_line, None)
                        else:
                            check_from_line = 0
                            skipped = f
                        # Skip n lines, i.e. start at index n
                        for i, line in enumerate(skipped, check_from_line):
                            if magic_text in line:
                                logging.info('magic text ' + magic_text +
                                             ' is in ' + name +
                                             ' in line '+str(i+1))
                            file_dict[name] = i
                except IOError as exc:
                    logging.error('Error:'+exc)
        else:
            logging.warning("Given directory does not exist.")
            time.sleep(polling_interval)


if __name__ == "__main__":
    if len(sys.argv) < 5:
        logging.error("Not all the args were passed.")
        sys.exit(1)
    main(sys.argv[1:])
