import better_logging
controller = better_logging.Controller("test.log")
logger = better_logging.Logger("test")
logger.info("example")
