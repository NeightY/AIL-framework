#!/usr/bin/env python2
# -*-coding:UTF-8 -*
"""
    Template for new modules
"""

import time
import re
from pubsublogger import publisher
from packages import Paste
from Helper import Process


def search_cve(message):
    filepath, count = message.split()
    paste = Paste.Paste(filepath)
    content = paste.get_p_content()
    # regex to find CVE
    reg_cve = re.compile(r'(CVE-)[1-2]\d{1,4}-\d{1,5}')
    # list of the regex results in the Paste, may be null
    results = set(reg_cve.findall(content))

    # if the list is greater than 2, we consider the Paste may contain a list of cve
    if len(results) > 0:
        print('{} contains CVEs'.format(paste.p_name))
        publisher.warning('{} contains CVEs'.format(paste.p_name))

        #send to Browse_warning_paste
        p.populate_set_out('cve;{}'.format(filepath), 'BrowseWarningPaste')
        #Send to duplicate
        p.populate_set_out(filepath, 'Duplicate')

if __name__ == '__main__':
    # If you wish to use an other port of channel, do not forget to run a subscriber accordingly (see launch_logs.sh)
    # Port of the redis instance used by pubsublogger
    publisher.port = 6380
    # Script is the default channel used for the modules.
    publisher.channel = 'Script'

    # Section name in bin/packages/modules.cfg
    config_section = 'Cve'

    # Setup the I/O queues
    p = Process(config_section)

    # Sent to the logging a description of the module
    publisher.info("Run CVE module")

    # Endless loop getting messages from the input queue
    while True:
        # Get one message from the input queue
        message = p.get_from_set()
        if message is None:
            publisher.debug("{} queue is empty, waiting".format(config_section))
            time.sleep(1)
            continue

        # Do something with the message from the queue
        search_cve(message)

