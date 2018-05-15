import thread
import threading
import time
import io
import Queue
import atexit
import ctypes
import datetime

__libc = ctypes.cdll.LoadLibrary('libc.so.6')
__log_levels_ints = {
        0: "DEBUG",
        1: "INFO",
        2: "WARN",
        3: "ERROR",
        4: "FATAL"
        }
__log_levels_strings = {
        "DEBUG": 0,
        "INFO": 1,
        "WARN": 2,
        "ERROR": 3,
        "FATAL": 4
        }
__logging_queue = Queue.Queue()
__logging_filename = None
__logging_enabled = 0
__logging_controller = None


def __get_thread_id():
    return __libc.syscall(186)


def __drain_logging_queue():
    global __logging_enabled
    global __logging_filename
    global __logging_queue
    global __controller_default_level
    while not __logging_filename and not __logging_enabled == 2:
        time.sleep(0.25)
    with io.open(__logging_filename, mode='a+', encoding='utf-8') as log_file:
        while __logging_enabled == 1 or not __logging_queue.empty():
            try:
                log_this = __logging_queue.get(timeout=0.25)
                if log_this[0] < __controller_default_level:
                    continue
                cur_time = datetime.datetime.now().strftime("%a %b %d %Y %H:%M:%S.%f")
                log_file.write(u'{3: <5} {0} [{1:x}] ({2}) {4}\n'.format(
                    cur_time,
                    log_this[1],
                    log_this[2],
                    __log_levels_ints[log_this[0]],
                    log_this[3]))
            except Exception:
                pass


__logging_thread = threading.Thread(target=__drain_logging_queue)
__logging_thread.setDaemon(True)
__logging_thread.start()


def __stop_logging():
    global __logging_enabled
    global __logging_thread
    __logging_enabled = 2
    __logging_thread.join()


atexit.register(__stop_logging)
__controller_default_level = 0


class Controller(object):
    def __init__(self, filename, default_level="INFO"):
        if globals()['__logging_filename'] is None:
            globals()['__logging_filename'] = filename
        if not globals()['__logging_enabled']:
            globals()['__logging_enabled'] = 1
        self.thread_id = globals()['__get_thread_id']()
        if globals()['__logging_controller'] is None:
            globals()['__logging_controller'] = self
        else:
            raise RuntimeError("There can only be one logging controller")
        if not globals()['__logging_enabled']:
            globals()['__logging_enabled'] = 1
        globals()['__controller_default_level'] = globals()['__log_levels_strings'][default_level]


class Logger(object):
    def __init__(self, sub_system, default_level="INFO"):
        if globals()['__logging_controller'] is None:
            raise RuntimeError(
                    "A logger instance cannot exist without a controller")
        self.thread_id = globals()['__get_thread_id']()
        self.sub_system = sub_system
        self.default_level = globals()['__log_levels_strings'][default_level]

    def log(self, level, message):
        if level < self.default_level:
            return
        globals()['__logging_queue'].put((level,
                                          self.thread_id,
                                          self.sub_system,
                                          message))

    def debug(self, message):
        self.log(0, message)

    def info(self, message):
        self.log(1, message)

    def warn(self, message):
        self.log(2, message)

    def error(self, message):
        self.log(3, message)

    def fatal(self, message):
        self.log(4, message)

