import time
import multiprocessing

def normal_logging():
    with open('test_og.log', "w") as log_file:
        for i in xrange(100000):
            log_file.write(u'{3: <5} {0} [{1:x}] ({2}) {4}\n'.format(
                    time.asctime(),
                    0, "test", "INFO", "message"))
t0 = time.time()
threads = []
for i in xrange(10):
    threads.append(multiprocessing.Process(target=normal_logging))
for t in threads:
    t.start()
for t in threads:
    t.join()
t1 = time.time()
print "printing", t1-t0

import better_logging
controller = better_logging.Controller("test.log")

def better_logging_comp():
    logger = better_logging.Logger("test")
    for i in xrange(100000):
        logger.info("message")
t0 = time.time()
threads = []
for i in xrange(10):
    threads.append(multiprocessing.Process(target=better_logging_comp))
for t in threads:
    t.start()
for t in threads:
    t.join()
t1 = time.time()
print "better_logging", t1-t0

import logging
logging.basicConfig(filename="test_logging.log", level=logging.DEBUG)

def logging_comp():
    for i in xrange(100000):
        logging.debug("message")
t0 = time.time()
threads = []
for i in xrange(10):
    threads.append(multiprocessing.Process(target=logging_comp))
for t in threads:
    t.start()
for t in threads:
    t.join()
t1 = time.time()
print "logging", t1-t0
