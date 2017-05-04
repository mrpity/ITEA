import configparser
import paramiko
import pprint
import argparse

class RUN_SSH:

    def __init__(self, filename, cmd: str, ssh_user):

        self.filename = filename
        self.username_ = ssh_user
        self.cmd_ = cmd

        self.config = self.get_config()
        self.config_servers = 'servers'
        self.whirl_zone = self.config['DEFAULT']['zone']
        self.env_list = self.config['DEFAULT']['env_list']

        self.servers= []
        self.get_servers()

    def __repr__(self):
        return "{}".format([server for server in self.servers])

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
        for env in self.env_list.split(','):
            server_list_ = []
            for item in self.config['{}'.format(env)]['{}'.format(self.config_servers)].split(','):
                server_list_.append(item.strip())
            self.servers += server_list_
            print("Server list: {}, for ENV:{}".format(server_list_, env))

    def ssh_execute(self):

        ssh = self.ssh_instance()
        for item in self.servers:
            server = "{}".format(item) + "." + self.whirl_zone
            try:
                ssh.connect(hostname='{}'.format(server), username='{}'.format(self.username_), timeout=3.0)
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('{}'.format(self.cmd_), get_pty=True)
                pprint.pprint("Executed on {}, stdout: {}".format(server, ssh_stdout.readlines()))
            except Exception:
                print(Exception, "Could not connect to host {}".format(server))

if __name__ == '__main__':

    ### Parse CLI vars
    def createParser():
        parser = argparse.ArgumentParser()
        #parser.add_argument('-u', '--user_name',default='dkhodakivsky', help='Set ssh user name')
        #parser.add_argument('-c', '--cmd_shell', default='sudo rm -rf /opt/download/*; ls /opt/download/', help='Set cmd shell')
        parser.add_argument('-f', '--file_name', default='server_list.conf', help='Set name of file to save env vars')
        parser.add_argument('-u', '--user_name', required=True, help='Set ssh user name')
        parser.add_argument('-c', '--cmd_shell', default='sudo rm -rf /opt/download/*; ls /opt/download/', help='Set cmd shell')
        return parser

    parser = createParser()
    namespace = parser.parse_args()

    ### Set variables from CLI
    SSH_USER = namespace.user_name
    FILENAME = namespace.file_name
    CMD = namespace.cmd_shell
    print("The following CMD: {} will be executed".format(CMD))

    R = RUN_SSH(FILENAME, CMD, SSH_USER)
    R.ssh_execute()
    print(R)
