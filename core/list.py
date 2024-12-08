from threading import Lock


class ThreadSafeList():
    # constructor
    def __init__(self):
        # initialize the list
        self._list = list()
        # initialize the lock
        self._lock = Lock()

    # add a value to the list
    def append(self, value):
        # acquire the lock
        with self._lock:
            # append the value
            self._list.append(value)

    # extend the list
    def extend(self, data):
        # acquire the lock
        with self._lock:
            # extend with new list
            self._list.extend(data)

    # remove and return the last value from the list
    def pop(self):
        # acquire the lock
        with self._lock:
            # pop a value from the list
            return self._list.pop()

    # remove value from the list
    def remove(self, value):
        # acquire the lock
        with self._lock:
            # pop a value from the list
            return self._list.remove(value)

    # read a value from the list at an index
    def __getitem__(self, index):
        # acquire the lock
        with self._lock:
            # read a value at the index
            return self._list[index]

    # return the number of items in the list
    def length(self):
        # acquire the lock
        with self._lock:
            return len(self._list)

    def __str__(self):
        return str(self._list)
