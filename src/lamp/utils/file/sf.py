# -*- coding: utf-8 -*-
import os
import fcntl
import contextlib
from ilock import ILock
from lamp.log import log


class SharedFile(object):
    def __init__(self, name):
        self.name = name

    def exclusive_create(self, data_f):
        with ILock(self.name + '.lock'):
            if self.exist():
                return

            with open(self.name, 'w') as f:
                data = data_f()
                f.write(data)

    def exist(self):
        return os.path.isfile(self.name)

    @contextlib.contextmanager
    def open_read(self):
        with open(self.name, 'r') as f:
            yield f


def test_main():
    def foo():
        import time
        time.sleep(10)
        return '1234567890\n'
    import os
    sf = SharedFile(os.path.expanduser('~/temp/sf'))
    sf.exclusive_create(foo)
    with sf.open_read() as f:
        data = f.read()
        print(data)

if __name__ == '__main__':
    test_main()
