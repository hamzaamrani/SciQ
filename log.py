# This file defines a decorator '@log_to()' that logs every call to a
# function, along with the arguments that function was called with. It
# takes a logging function, which is any function that accepts a
# string and does something with it. A good choice is the debug
# function from the logging module. A second decorator '@logdebug' is
# provided that uses 'logging.debug' as the logger.

from __future__ import print_function
from functools import wraps
from inspect import getcallargs, getfullargspec
from collections import OrderedDict
from collections.abc import Iterable
from itertools import chain


class Log(object):

    def __init__(self, logger_func=None, print_self=False):
        if logger_func is None:
            self.logger_func = lambda x: x
        else:
            self.logger_func = logger_func
        self.print_self = print_self

    def _flatten(self, l):
        """Flatten a list (or other iterable) recursively"""
        for el in l:
            if isinstance(el, Iterable) and not isinstance(el, str):
                for sub in self.flatten(el):
                    yield sub
            else:
                yield el

    def _getargnames(self, func):
        """Return an iterator over all arg names, including nested arg names and varargs.
        Goes in the order of the functions argspec, with varargs and
        keyword args last if present."""
        (args_names, varargs_names, varkws_names, _,
         kwonlyargs_names, _, _) = getfullargspec(func)
        if not self.print_self:
            args_names.remove("self")
        return chain(
            self._flatten(args_names),
            filter(None, [varargs_names, varkws_names]),
            self._flatten(kwonlyargs_names))

    def _getcallargs_ordered(self, func, *args, **kwargs):
        """Return an OrderedDict of all arguments to a function.
        Items are ordered by the function's argspec."""
        argdict = getcallargs(func, *args, **kwargs)
        return OrderedDict((name, argdict[name])
                           for name in self._getargnames(func))

    def _describe_call(self, func, *args, **kwargs):
        for argname, argvalue in self._getcallargs_ordered(
                func, *args, **kwargs).items():
            yield "\t%s = %s" % (argname, repr(argvalue))

    def __call__(self, func):
        """A decorator to log every call to function (function name and arg values).
        logger_func should be a function that accepts a string and logs it
        somewhere. The default is logging.debug.
        If logger_func is None, then the resulting decorator does nothing.
        This is much more efficient than providing a no-op logger
        function: @log_to(lambda x: None).
        """
        @wraps(func)
        def decorator(*args, **kwargs):
            self.logger_func("Calling %s with args:" % func.__name__)
            for line in self._describe_call(func, *args, **kwargs):
                self.logger_func(line)
            return func(*args, **kwargs)

        return decorator
