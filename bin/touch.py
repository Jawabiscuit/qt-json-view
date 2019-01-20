#! /usr/bin/env python
import os


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


def touch_py3(fname, mode=0o666, dir_fd=None, **kwargs):
    flags = os.O_CREAT | os.O_APPEND
    with os.fdopen(os.open(fname, flags=flags, mode=mode, dir_fd=dir_fd)) as f:
        os.utime(f.fileno() if os.utime in os.supports_fd else fname,
            dir_fd=None if os.supports_fd else dir_fd, **kwargs)


if __name__ == "__main__":
    import sys

    try:
        if sys.version[0] == "2":
            touch(sys.argv[1])
        elif sys.version[0] == "3":
            touch_py3(sys.argv[1])
    except:
        import traceback
        traceback.print_exc(sys.stderr)
