import os
import sys
from multiprocessing import Process
import pytest
import time

PYTEST_DIR = os.path.dirname(__file__)
ROOT = os.path.dirname(os.path.dirname(PYTEST_DIR))
MLOC_DIR = os.path.join(ROOT, "mloc")

sys.path.insert(0, MLOC_DIR)

from mloc.mloc import run_mloc  # noqa


class Env:
    def __init__(self):
        self.p = Process(target=run_mloc)

    def start(self):
        self.p.start()
        time.sleep(2)

    def stop(self):
        if not self.p:
            return
        self.p.terminate()
        self.p = None


@pytest.yield_fixture(autouse=True, scope="function")
def mloc_env():
    env = Env()
    yield env
    env.stop()
