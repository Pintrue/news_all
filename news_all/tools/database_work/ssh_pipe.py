# -*- coding: utf-8 -*-
# @File    : ssh_pipe.py
import getpass
from sshtunnel import SSHTunnelForwarder

SSH_HOST = '39.105.14.86'  # 第一台服务器外网IP
SSH_PORT = 22

WORK_MACHINE = ['172.16.0.111', '172.16.0.116', '172.16.0.115', '172.16.0.171', '172.16.0.172',
                '172.16.0.173']  # todo 爬虫服务器内网IP
OUT_NET_HOST = ['192.168.42.144', '127.0.0.1']  # 外网host


class SSHUsers(object):
    """ssh隧道用户信息
    users 的 key必须是当前登录操作系统的用户名
    """
    users = {
        'wjq': {
            # 'keyfile': '/Users/wangjingqiong/.ssh/id_rsa',  # Linux 或 Mac
            'ssh_user': 'root',
            'ssh_pw': '2aYGYr3wQ717aT%IGzRH@C'
        },
    }


def create_ssh_server(remote_host, remote_port):
    """
    创建ssh服务
    :param remote_host:     str                     远端ip
    :param remote_port:     int                     远端port
    :return:                SSHTunnelForwarder      ssh tunnel实例
    """
    
    ssh_user_name = getpass.getuser()
    print('-------ssh_user_name:%s-------' % ssh_user_name)
    ssh_user = SSHUsers.users.get(ssh_user_name, '')
    
    # if not ssh_user.get('keyfile', ''):
    #     raise Exception('登陆跳板机必须使用ssh_keyfile')
    
    ssh_tunnel_params = {
        'ssh_address_or_host': (SSH_HOST, SSH_PORT),
        # 'ssh_pkey': ssh_user['keyfile'],
        'ssh_username': ssh_user['ssh_user'],
        'ssh_password': ssh_user['ssh_pw'],
        'remote_bind_address': (remote_host, remote_port),
    }
    
    ssh_server = SSHTunnelForwarder(**ssh_tunnel_params)
    ssh_server.start()
    print("ssh - server建立完成")
    return ssh_server


if __name__ == "__main__":
    s = create_ssh_server('172.16.0.116', 22)
    s.stop()
