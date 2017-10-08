# Exploit for SuiteCRM (7.2.2) Post-Auth File Upload/Race Condition Remote Code Execution
In SuiteCRM Version 7.2.2-max, [the vulnerability I discovered in SuiteCRM 7.2.1 involving a post-auth shell upload RCE](https://github.com/XiphosResearch/exploits/tree/master/suiteshell) was patched. The patch involved verifying the image uploaded **after** writing it to disc, and if it failed the image upload check, unlink() was called on the image. Also, the .phtml file extension we were using was added to the blacklist.  

Upon reading the patch, [I let the devs know that it introduced a race condition, however my comments seemingly were not taken onboard at the time](https://github.com/salesagility/SuiteCRM/commit/b1b3fd61c7697ad2073cd253d31c9462929e7bb5#commitcomment-11281062), and the buggy patch was committed and added to the 7.2.2-max release. I decided to try exploit the race condition, and here we are :)  

Basically, how this exploit works is not much different to the prior exploit, and the PoC is simply a modified version of it. The file uploaded (this time using a .pht file extension, because blacklisting sucks), exists on disc for a mere split second before it fails the image validity check and unlink() is called on it. So we must "beat the unlink call" and request our backdoor file before it gets deleted. The most effective way of doing this is to repeatedly upload the file in one thread, while requesting it in another. The PoC I have written here does this in a rather crude manner, landing us with a shell within about seven to ten seconds.  

To optimize the exploit, instead of logging in every single time we want to pwn the box, we simply log in once, and reuse the session we get from the server. This means we can do the upload step in a far "tighter loop", and generally speeds things up (without this optimization, we were getting a shell in about a minute or so).  

## Video of Exploitation
[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/eHVIg5eoYNc/0.jpg)](http://www.youtube.com/watch?v=eHVIg5eoYNc)

## Using the exploit
Using this exploit is very simple. You simply supply it with the URL of the vulnerable SuiteCRM instance, an admin username and password, your payload file (back_python.php), and a callback host and port where you would like it to send a reverse PTY shell. Due to it not exactly exiting properly (due to my horrible misuse of threads) after popping a shell, you will want to kill -9 the exploit process once you get a callback. I intend to eventually get around to fixing this, but for a quick, filthy, and reliable PoC, this is not really needed.

## Licence
Licenced under the [WTFPL](http://www.wtfpl.net)
