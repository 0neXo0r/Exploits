# Exploit for CVE-2015-7808 - vBulletin 5.x.x unserialize() Remote Code Execution
This is an exploit for the PHP Object Injection vulnerability recently disclosed in the reasonably popular vBulletin forum software. Our exploit does some basic information gathering before firing off the usual payload to give us a reverse connecting PTY shell. Currently, we only have a Python payload available, but that might change sometime.

## Usage:
You just need to specify the target, payload, and callback host/port. Example use is outlined in the video below.

## Video of Exploitation
[![vbullshit](http://img.youtube.com/vi/LT_HLS9rpC8/0.jpg)](https://www.youtube.com/watch?v=LT_HLS9rpC8)

## Licence
Licenced under the [WTFPL][wtfpl]

[wtfpl]: http://www.wtfpl.net/
