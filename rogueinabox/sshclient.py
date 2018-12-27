#!/usr/bin/env python

# this class sets up simple client behavior for Rogue over an SSH connection using pexpect

import paramiko
import getpass

class RogueSSHClient(object):
    def __init__(self):
        self.s = None
        
    def connect_and_start(self, hostname, username, password, port = 1988, rogue_path = 'rogue5.4.4-ant-r1.1.4', rogue_command = 'rogue'):
    
        self.s = paramiko.SSHClient()
        
        self.s.load_system_host_keys()
        self.s.set_missing_host_key_policy(paramiko.WarningPolicy)
        
        print('Attempting to connect over SSH...')
        
        self.s.connect(hostname, port=port, username=username, password=password)
        
        print('Attempting to invoke_shell()')
        
        self.channel = self.s.invoke_shell()
        
        print('channel : '.format(self.channel))
        
        print('invoke_shell() completed')
        
        #self.stdin = self.channel.makefile('wb')
        #self.stdout = self.channel.makefile('r')
        
        self.channel.send('uptime\n')
        print(self.channel.recv(65000))
        
        self.channel.send('cd {}'.format(rogue_path) + '\n')
        print(self.channel.recv(65000))
        
        self.channel.send('./{} && exit'.format(rogue_command) + '\n')
        print(self.channel.recv(65000))
        
        #self.s.close()
        
    def is_running(self):
        return self.s.get_transport().is_active()
        
    def read(self, size):
        return self.channel.recv(size)
     
    def write(self, str):
        return self.channel.send(str)
        
    def kill(self):
        self.s.close()
        self.s = None
