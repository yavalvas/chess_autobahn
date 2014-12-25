# -*- coding: utf-8 -*-
import sys

from twisted.python import log as _txlog

def debug(msg, *fmt):
    """Отладочное сообщение."""
    _txlog.msg(_msg(msg, fmt))

def _msg(msg, fmt):
    if fmt:
        msg = msg % fmt

    if isinstance(msg, unicode):
        try:
            msg = msg.encode(sys.stdout.encoding)
        except UnicodeError:
            msg = repr(msg) + "\n\t^^^ unicode error during converting to %s ^^^" % sys.stdout.encoding

    return msg