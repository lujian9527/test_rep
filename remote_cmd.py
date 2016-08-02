#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pexpect
import sys


def ssh_cmd(ip, cmd):
    ssh = pexpect.spawn('/usr/bin/ssh -l root %s -o ConnectTimeout=2 "%s"' % (ip, cmd))
    try:
        i = ssh.expect(['[P|p]assword:', '(yes/no)?'], timeout=3)
        if i == 0:
            return "need password"
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('password: ')
            return "need password"
        ssh.sendline(cmd)
        r = ssh.read()
        return r
    except pexpect.EOF:
        return ssh.before
    except pexpect.TIMEOUT:
        return "timeout"
    finally:
        ssh.close()


def handler():
    file = open("/tmp/lj/ip.lst", "r")
    while 1:
        ip = file.readline()
        if not ip:
            break
        print ip.strip() + "-->" + str(ssh_cmd(ip, sys.argv[1]))
    file.close()


if __name__ == "__main__":
    handler()
