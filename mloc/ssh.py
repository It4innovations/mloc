import paramiko

from .settings import (PBS_HOSTNAME, PBS_SSH_KEY_PASSWORD, PBS_SSH_KEY_PATH,
                       PBS_SSH_PORT, PBS_SSH_USERNAME)


class SSHSession:
    def __init__(self):
        self.sess = paramiko.SSHClient()
        self.sess.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def open(self):
        pkey = paramiko.RSAKey.from_private_key_file(filename=PBS_SSH_KEY_PATH, password=str(PBS_SSH_KEY_PASSWORD))
        self.sess.connect(PBS_HOSTNAME, PBS_SSH_PORT, PBS_SSH_USERNAME, pkey=pkey)
        
    def cmd(self, cmd):
        (stdin, stdout, stderr) = self.sess.exec_command(cmd)
        stderr = stderr.readlines()
        stdout = stdout.readlines()
        return stdout, stderr

    def close(self):
        self.sess.close()
