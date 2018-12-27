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
        
        self.s.connect(hostname, port=port, username=username, password=password)
        
        self.channel = self.s.invoke_shell()
        
        self.stdin = self.channel.makefile('wb')
        self.stdout = self.channel.makefile('r')
        
        self.stdin.write('uptime\n')
        self.stdin.flush()
        
        self.stdin.write('cd {}'.format(rogue_path) + '\n')
        self.stdin.flush()
        
        self.stdin.write('{} && exit'.format(rogue_command) + '\n')
        self.stdin.flush()
        
        #self.s.close()
        
    def is_running(self):
        return self.s.get_transport().is_active()
        
    def read(self, size):
        return self.stdout.read(size)
     
    def write(self, str):
        return self.stdin.write(str)
        
    def kill(self):
        self.s.close()
        self.s = None
