import signal
import logging
import time
import os
import sys
import re
# some other changes
exit_flag = False
start_time = time.time()
# some changes - kavitha
logging.basicConfig(filename='log.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically it just sets a global flag, and main() will exit it's loop if the signal is trapped.
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
    exit_flag = True


def main(src_dir, magic_text):
    # Hook these two signals from the OS ..
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends either of these to my process.

    if not exit_flag:
        logging.debug('Program has started.')
    while not exit_flag:
        # Do my long-running stuff
        if os.path.isdir(src_dir):
            pattern = re.compile(magic_text)  # Magic text to search for

            # obtain list of files in directory
            for yum_files in os.listdir(src_dir):
                # join the full path with the names of the files.
                files = os.path.join(src_dir, yum_files)
                strng = open(files)  # We need to open the files
                for lines in strng.readlines():  # We then need to read the files
                    if re.search(pattern, lines):  # If we find the pattern we are looking for
                        logging.info('magic text in ' + file +
                                     ' in line ' + str(i))
        else:
            logging.warning("Given directory does not exist.")
            time.sleep(5)
        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        time.sleep(2)


if __name__ == "__main__":
    print sys.argv
    if len(sys.argv) < 4:

    main()
