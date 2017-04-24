import configparser
import paramiko


def get_config(filename):
    config = configparser.ConfigParser()
    config.read('{}'.format(filename))
    return config

def ssh_instance():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    return ssh

def get_servers(env_list):
    print("ENV list: {}".format(env_list))
    for env in env_list:
        server_list = []
        for item in config['{}'.format(env)]['servers'].split(','):
            server_list.append(item.strip())
        ssh = ssh_instance()   ## ssh instance
        print("Server list: {}, for ENV:{}".format(server_list, env))
        ssh_execute(ssh, server_list)                               ## ssh execute

def ssh_execute(ssh, server_list):
    username_ = "dkhodakivsky"
    cmd_ = "echo 'test_paramiko' > /tmp/test_paramiko.txt"
    whirl_zone = config['DEFAULT']['zone']

    for item in server_list:
        server = "{}".format(item) + "." + whirl_zone
        try:
            ssh.connect(hostname='{}'.format(server), username='{}'.format(username_))
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('{}'.format(cmd_))
            print(server, ssh_stdout)
        except Exception:
            print(Exception, "Could not connect to host {}".format(server))

#if '__name__' == '__main__':

FILENAME = "server_list.conf"
ENV_LIST = ['PITY', 'QA1', 'QA2']

config = get_config(FILENAME)

get_servers(ENV_LIST)