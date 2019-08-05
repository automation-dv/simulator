import threading
sem = threading.Semaphore()


class ServerStats:
    global server_stats, total, accurate, inaccurate

    server_stats = {}
    total = accurate = inaccurate = 0

    @staticmethod
    def reset_stats():
        global total
        global accurate
        global inaccurate
        global server_stats
        server_stats = {}
        total = accurate = inaccurate = 0

    @staticmethod
    def add_total(val):
        global total
        sem.acquire()
        total += val
        sem.release()

    @staticmethod
    def add_accurate():
        sem.acquire()
        global accurate
        accurate += 1
        sem.release()

    @staticmethod
    def add_inaccurate():
        sem.acquire()
        global inaccurate
        inaccurate += 1
        sem.release()

    @staticmethod
    def get_total():
        global total
        return total

    @staticmethod
    def get_accurate():
        global accurate
        return accurate

    @staticmethod
    def get_inaccurate():
        global inaccurate
        return inaccurate

    @staticmethod
    def get_server_stats():
        global total
        global accurate
        global inaccurate
        global server_stats
        server_stats = {'Total': total, 'Accurate': accurate, 'Inaccurate': inaccurate}

        return server_stats

