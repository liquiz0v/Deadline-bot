from typing import List
from threading import Thread
from time import sleep


class Conv:
    def __init__(self):
        self.threads: List[Thread] = []

    def add_not(self, time_to_sleep, func, args) -> int:
        """
        add thread with function func(args) to canvayor
        """
        myfunc = self.__wrap(time_to_sleep, func, args)
        thr = Thread(target=myfunc)
        thr.start()
        id = thr.ident
        self.threads.append(thr)

        return id

    def rm_not(self, id: int) -> bool:
        """
        remove thread by its id (Thread.ident)
        """
        for t in self.threads:
            if t.ident == id:
                t._stop()
                self.threads.remove(t)
                return True

        return False

    def reset(self) -> None:
        """
        stop all threads and delte them
        """
        for t in self.threads:
            t._stop()
            self.threads.remove(t)

    def __wrap(self, time_to_sleep: int, func, args):
        """
        function to start a thread with.
        \n:time_to_sleep = due_time - current_time
        """

        def inner():
            sleep(time_to_sleep)
            func(args)

        return inner
