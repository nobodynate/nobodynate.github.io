# Nibbles

## Recon
Tags for [this box](https://app.hackthebox.com/machines/121) are:  
> - File Misconfiguration
> - Web

Difficulty:
> Easy

Port scan shows an Apache webserver running on port 80. The site appears to be a static HTML page. In the HTML comments there is a reference to the `/nibbleblog/` site.  

Feroxbuster agains this directory found `/admin/` as wel as `/admin.php` (a login page). 

## Exploitation
Searched for "nibbles" in metasploit and found `exploit/multi/http/nibbleblog_file_upload`  
This exploit matches our target application's version. Unfortunately, this exploit requires authentication.

### Getting help

Getting credentials had me stuck. I tried SQL injections and bruteforce. I reviewed the enumeration material multiple times to make sure I wasn't missing something. Finally I looked at a walkthrough. The author of the walkthrough was struggling too and he ended up just guessing the name of the box as the password. Turns out the password is the name of the box.

> User: `admin`  
> pass: `nibbles`

With credentials in hand, the nibbleblog exploit grants a shell as a normal user.

## Privilege Escalation

The host is running Ubuntu 16.04.3. When searched in metasploit there is the following module: `exploit/linux/local/bpf_sign_extension_priv_esc` which grants root access.


## Reflect/Compare

Both paths were mostly the same at first:

> Scan identified Apache:80  
> HTML comments disclosed `/nibbleblog/` site  
> Feroxbuster found `/admin.php` logon page.  
> Found `multi/http/nibbleblog_file_upload`  

This is where we split
My path:

> Got creds from walkthrough.  
> `nibbleblog_file_upload` grants user access.  
>  Found `linux/local/bpf_sign_extension_priv_esc`  by searching for PE on Ubuntu 16.04.3  
>  grans root access.  

HTB writeup:

> Guessed the correct password  
> `nibbleblog_file_upload` grants user access  
> `sudo -l` revealed the ability to run `/home/nibbler/personal/stuff/monitor.sh`  
> `bash -i > monitor.sh`  
> `sudo monitor.sh`  
> grants root  


### Analysis
I failed to guess the password (which was the name of the blog). I remember seeing `monitor.sh` and attempting to exploit it but I wasn't able to get it to work. I think the missing piece here was to create the script on the attack machine then upload to the victim - I was trying to create the script on the victim, which wasn't working.

#### Lessons Learned
> Sometimes you can upload a file but not create one.  
> If I focused more on the CyberKillchain, maybe this would have fell under "delivery" and I would have seen the other channel (upload vs direct write.)  