# Bounty

Port 80 is the only one open.

This webserver is running IIS 7.5. Dirbuster finds `/transfer.aspx` and `/uploadedfiles/`

I tested a few uploads, but get a message that the file can't be uploaded. Trying a bunch of differnent extensions I found the only working one is `.config`

PayloadAllTheThings has this [web.config shell](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/Configuration%20IIS%20web.config/web.config) so we upload it and get command execution.

I used Powershell-InvokeTCP to get a shell.

First I noticed we have `SEImpersonate` Enabled, which means I can try JuicyPotato.

`Systeminfo` tells us this is Windows Server 2008 R2. Based on a google search I found `MS15-032` may be applicable. However, I was not able to exploit this through powershell or metasploit.

## Privesc
Juicy Potato worked. I was able to get a shell as System