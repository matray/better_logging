import time

t0 = time.time()
with open('test_og.log', "w") as log_file:
    for i in xrange(100000):
        log_file.write(u'{3: <5} {0} [{1:x}] ({2}) {4}\n'.format(
                time.asctime(),
                0, "test", "INFO", "message"))
t1 = time.time()
print "printing", t1-t0

import better_logging
controller = better_logging.Controller("test.log")
logger = better_logging.Logger("test")
t0 = time.time()
for i in xrange(100000):
    logger.info("message")
t1 = time.time()
print "better_logging", t1-t0

import logging
logging.basicConfig(filename="test_logging.log", level=logging.DEBUG)
t0 = time.time()
for i in xrange(100000):
    logging.debug("message")
t1 = time.time()
print "logging", t1-t0
