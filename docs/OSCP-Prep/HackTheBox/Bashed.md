# Bashed

A port scan shows only port 80 is open. I went to the webpage and see the site is talking about phpbash. I click the github link and the page explains phpbash is a webshell.

Dirbuster found `/dev/` and there are 2 instances of the phpbash program. These give RCE as the `www-data` user.

A more formal shell is obtained by putting a python reverse shell in a .py file and executing it using phpbash. I couldn't get bash rev shells working for some reason.

Once I'm on the box, I ran `sudo -l` as always. It tells me I can run any command as the `scriptmanager` user. At this point I might as well elevate the shell:

```bash
sudo -u scriptmanager /bin/bash
```

The user flag `/home/arrexel/user.txt` is readable by scriptmanager

Linpeas highlighted the kernel version so I turned to searchsploit:

```bash
searchsploit linux kernel ubuntu 4.4.0-62
```

EDB-45010 is a local priv esc for this kernel. I compiled with `gcc` on kali then transferred the binary over. It worked!

The root flag is at `/root/root.txt`




