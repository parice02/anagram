# -*- conding: utf8 -*-

"""
@author: Muhammed Zeba (parice02)
"""

"""
Source: https://saladtomatonion.com/blog/2014/12/16/mesurer-le-temps-dexecution-de-code-en-python/
"""

import time


class Timer(object):
    """ """

    def __enter__(self):
        self.start()
        # __enter__ must return an instance bound with the "as" keyword
        return self

    def __exit__(self, *args, **kwargs):
        # There are other arguments to __exit__ but we don't care here
        self.stop()

    def start(self):
        if hasattr(self, "interval"):
            del self.interval
        self.start_time = time.time()

    def stop(self):
        if hasattr(self, "start_time"):
            self.interval = time.time() - self.start_time
            del self.start_time  # Force timer re-init


class LoggerTimer(Timer):
    """ """

    @staticmethod
    def default_logger(msg):
        print(msg)

    def __init__(self, prefix="", func=None):
        # Use func if not None else the default one
        self.f = func or LoggerTimer.default_logger
        # Format the prefix if not None or empty, else use empty string
        self.prefix = f"{prefix}" if prefix else ""

    def __call__(self, func):
        # Use self as context manager in a decorated function
        def decorated_func(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return decorated_func

    def stop(self):
        # Call the parent method
        super(LoggerTimer, self).stop()
        # Call the logging function with the message
        self.f(f"{self.prefix}: {self.interval}")
