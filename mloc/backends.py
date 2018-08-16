from multiprocessing import Process

class Local:
    @staticmethod
    def _execute(*args, **kwargs):
        op = args[0]
        op(**kwargs)

    @staticmethod
    def execute(op, **kwargs):
        p = Process(target=Local._execute, args=(op,), kwargs=kwargs)
        p.start()
