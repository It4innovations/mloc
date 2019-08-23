import logging
from multiprocessing import Process, Queue
from threading import Thread

from bson.objectid import ObjectId

from .states import General


class LocalBackend:
    def __init__(self, db, single_run=False):
        self.q = Queue()
        t = Thread(target=LocalBackend.state_handler, args=(self.q, db, single_run))
        t.start()

    @staticmethod
    def state_handler(q, db, single_run):
        while True:
            resource, _id, update = q.get()
            print("New update!!!!!: {}".format(update))
            logging.debug(
                '{} {}: updating {}'.format(resource, _id, update))
            db.update_item(resource, _id, update)
            if update['state'] == str(General.FINISHED) and single_run==True:
                break

    def _execute(self, q, op, _id, resource, **kwargs):
        q.put((resource, _id, {'state': str(General.RUNNING)}))
        try:
            print("!!!!")
            logging.debug(
                '{} {}: executing operation {}'.format(resource, _id, op))
            result = op(_id=_id, **kwargs)
            if type(result) == dict:
                update = result
            else:
                update = {}
            update['state'] = str(General.FINISHED)
            q.put((resource, _id, update))
            print("#######")
        except Exception as e:
            logging.error('{} {}: error {}'.format(resource, _id, str(e)))
            update = {'state': str(General.ERROR), "error": str(e)}
            q.put((resource, _id, update))

    def execute(self, op, _id, resource, **kwargs):
        p = Process(target=self._execute,
                    args=(self.q, op, _id, resource),
                    kwargs=kwargs)
        p.start()

    def _execute_pbs(self, q, op, _id, resource, **kwargs):
        q.put((resource, _id, {'state': str(General.QUEUED)}))
        try:
            print("!!!!PBS")
            logging.debug(
                '{} {}: executing operation {}'.format(resource, _id, op))
            result = op(_id=_id, **kwargs)
            if type(result) == dict:
                update = result
            else:
                update = {}
            q.put((resource, _id, update))
            print("#######PBS")
        except Exception as e:
            logging.error('{} {}: error {}'.format(resource, _id, str(e)))
            update = {'state': str(General.ERROR), "error": str(e)}
            q.put((resource, _id, update))

    def execute_pbs(self, op, _id, resource, **kwargs):
        p = Process(target=self._execute_pbs,
                    args=(self.q, op, _id, resource),
                    kwargs=kwargs)
        p.start()
