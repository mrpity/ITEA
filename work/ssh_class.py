import configparser
import paramiko

class RUN_SSH:

    def __init__(self, filename, env_list: list, cmd: str):
        self.filename = filename
        self.env_list = env_list
        self.username_ = "dkhodakivsky"
        self.cmd_ = cmd
        self.config = self.get_config()
        self.config_servers = 'servers'
        self.whirl_zone = self.config['DEFAULT']['zone']

        self.get_servers()

    def get_config(self):
        config = configparser.ConfigParser()
        config.read('{}'.format(self.filename))
        return config

    def ssh_instance(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return ssh

    def get_servers(self):
        print("ENV list: {}".format(self.env_list))
        for env in self.env_list:
            server_list_ = []
            for item in self.config['{}'.format(env)]['{}'.format(self.config_servers)].split(','):
                server_list_.append(item.strip())
            ssh = self.ssh_instance()
            print("Server list: {}, for ENV:{}".format(server_list_, env))
            self.ssh_execute(ssh, server_list_)

    def ssh_execute(self, ssh, server_list):

        for item in server_list:
            server = "{}".format(item) + "." + self.whirl_zone
            try:
                ssh.connect(hostname='{}'.format(server), username='{}'.format(self.username_))
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('{}'.format(self.cmd_))
                print(server, ssh_stdout)
            except Exception:
                print(Exception, "Could not connect to host {}".format(server))

if __name__ == '__main__':

    FILENAME = "server_list.conf"
    ENV_LIST = ['PITY', 'QA1', 'QA2']
    CMD = "echo 'test_class_paramiko' > /tmp/test_paramiko.txt"
    R = RUN_SSH(FILENAME, ENV_LIST, CMD)
