from multiprocessing import Process, Queue
from threading import Thread
from states import General
from db import update_item

class Local:
    def __init__(self, db):
        self.q = Queue()
        t = Thread(target=Local.state_handler, args=(self.q, db))
        t.start()

    @staticmethod
    def state_handler(q, db):
        while True:
            resource, _id, update = q.get()
            update_item(db, resource, _id, update)

    def _execute(self, q, op, _id, resource, **kwargs):
        q.put((resource, _id, {'state': str(General.RUNNING)}))
        try:
            result = op(_id=_id, **kwargs)
            q.put((resource, _id, {'state': str(General.FINISHED), "result": str(result)}))
        except Exception as e:
            q.put((resource, _id, {'state': str(General.ERROR), "error": str(e.message)}))

    def execute(self, op, _id, resource, **kwargs):
        p = Process(target=self._execute,
                    args=(self.q, op, _id, resource),
                    kwargs=kwargs)
        p.start()
