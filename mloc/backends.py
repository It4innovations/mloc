from multiprocessing import Process, Queue
from threading import Thread
from states import General


class LocalBackend:
    def __init__(self, db):
        self.q = Queue()
        t = Thread(target=LocalBackend.state_handler, args=(self.q, db))
        t.start()

    @staticmethod
    def state_handler(q, db):
        while True:
            resource, _id, update = q.get()
            db.update_item(resource, _id, update)

    def _execute(self, q, op, _id, resource, **kwargs):
        q.put((resource, _id, {'state': str(General.RUNNING)}))
        try:
            result = op(_id=_id, **kwargs)
            if type(result) == dict:
                update = result
            else:
                update = {}
            update['state'] = str(General.FINISHED)
            q.put((resource, _id, update))
        except Exception as e:
            update = {'state': str(General.ERROR), "error": str(e)}
            q.put((resource, _id, update))

    def execute(self, op, _id, resource, **kwargs):
        p = Process(target=self._execute,
                    args=(self.q, op, _id, resource),
                    kwargs=kwargs)
        p.start()
