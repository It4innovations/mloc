import os

from .settings import (MONGO_DBNAME, MONGO_HOST, MONGO_PASSWORD, MONGO_PORT,
                       MONGO_USERNAME)
from .ssh import SSHSession


class PBS:
    @staticmethod 
    def _qsub(script_path, queue="qexp", walltime="01:00:00",
              nodes=1, account=None):
        cmd = ["qsub"]
        cmd.append("-q {}".format(queue))
        cmd.append("-l select={}".format(nodes))
        cmd.append("-l walltime={}".format(walltime))
        if account:
            cmd.append("-A {}".format(account))
        cmd.append("{}".format(script_path))
        return " ".join(cmd)

    @staticmethod 
    def _qdel(job_id):
        cmd = ["qdel"]
        cmd.append("{}".format(job_id))
        return " ".join(cmd)

    @staticmethod 
    def _qstat(job_id=None):
        cmd = ["qstat"]
        if jobid:
            cmd.append("{}".format(job_id))
        return " ".join(cmd)

    @staticmethod
    def _generate_fit_script_str(fit_id):
        script = """
        #!/bin/bash
        ml Python/3.6.1
        ml OpenMPI
        export MONGO_HOST={mongo_host}
        export MONGO_PORT={mongo_port}
        export MONGO_DBNAME={mongo_dbname}
        export MONGO_USERNAME={mongo_username}
        export MONGO_PASSWORD={mongo_password}
        python3 -m mloc.executor {fit_id}
        """.format(mongo_host=MONGO_HOST, mongo_port=MONGO_PORT,
                   mongo_dbname=MONGO_DBNAME, mongo_username=MONGO_USERNAME,
                   mongo_password=MONGO_PASSWORD, fit_id=fit_id)
        return script

    @staticmethod
    def submit_fit(fit_id, **kwargs):
        s = SSHSession()
        s.open()
        script = PBS._generate_fit_script_str(fit_id)
        print(script)
        script_path = os.path.join("/tmp", "mloc-fit-{}.pbs".format(fit_id))
        print(script_path)
        cmd1 = "echo -e '{}' > {}".format(script, script_path) 
        stdout, stderr = s.cmd(cmd1)
        print(stdout, stderr)
        cmd2 = PBS._qsub(script_path, **kwargs)
        stdout, stderr = s.cmd(cmd2)
        print(stdout, stderr)
        s.close

#PBS.submit_fit("5d5fefb6e762d67513d25805")
