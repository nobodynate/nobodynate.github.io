# Shocker

## Recon
Tags for [this box](https://app.hackthebox.com/machines/108) are: 
> - Perl
> - Injection
> - Web

Difficulty:
> Easy

Only 2 ports exposed: 2222 (ssh), and 80 (apache)

The running version of SSH doesn't have any public exploits, so it seems pretty obvious the target will be a website for this challenge.

## Enumeration
Nothing stood out from the scanning docs. I had to step back and really ask myself some fundamental questions to move forward on this one.

#### What does it do?

I've only been able to see the homepage `index.html` which appears to be a static page with a picture of a bug about to squash itself.

#### What language is it written in?

Based on some feroxbuster output (403 errors) the site seems to have the following filetypes `aspx`, `asp`, `jsp`, `php`.

#### What server software is the application running on?

Apache httpd 2.4.18 (Ubuntu)

### Getting help
I peaked at the walkthrough because I was lost.
No shocker - this machine was built to practice shellshock.  

On apache, the `cgi-bin` folder contains scripts. The scripts are accessed via web, run server side, then returned with an HTTP reply. Shellshock provides input that hijacks the server-side shell run. I also saw in the walkthrough that the target script is `/cgi-bin/user.sh`. 

But I want to prove this with a scan.

### fuzzing for shellshock
Found a shellshock endpoint by running
```bash
feroxbuster -u http://10.10.10.56:80/cgi-bin/ -t 10 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x "sh" -v -k -n -o /home/nate/hackthebox/shocker/results/scans/tcp80/tcp_80_http_feroxbuster_cgi-bin.txt
```
![[Pasted image 20220106200355.png]]

## Exploitation

![[Pasted image 20220106202024.png]]

![[Pasted image 20220106204959.png]]

I was able to get user.txt but not enough privs for root.txt

## Privilege Escalation

### Linpeas findings

> Sudo version 1.8.16

> ╔══════════╣ Executing Linux Exploit Suggester 2  
> ╚ https://github.com/jondonas/linux-exploit-suggester-2  
>   
> [1] af_packet  
> 	CVE-2016-8655  
> 	Source: http://www.exploit-db.com/exploits/40871  
> [2] exploit_x  
> 	CVE-2018-14665  
> 	Source: http://www.exploit-db.com/exploits/45697  
> [3] get_rekt  
> 	CVE-2017-16695  
> 	Source: http://www.exploit-db.com/exploits/45010  

> ╔══════════╣ Checking 'sudo -l', /etc/sudoers, and /etc/sudoers.d
> ╚https://book.hacktricks.xyz/linux-unix/privilege-escalation#sudo-and-suid
> Matching Defaults entries for shelly on Shocker:  
> env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin  
> 
> User shelly may run the following commands on Shocker:  
> (root) NOPASSWD: /usr/bin/perl 

Might be able to use the following from GTFO bins to get root.
```
sudo perl -e 'exec "/bin/sh";'
```

![[Pasted image 20220106210114.png]]


## Reflect/Compare
My Path:  
> Scan finds Apache `2.4.18` on port 80  
> Looked at walkthrough  
> Fuzz /cgi-bin/ to find endpoint vulnerable to Shellshock.
> Send webrequest with malicious header.  
> Got User  
> User can run `perl` as sudo  
> GTFO bins for `SUDO` and `perl`
> Root

HTB Walkthrough:
> Scan finds Apache on port 80  
> Fuzzed and found `cgi-bin` directory  
> Knows they're exploiting shellshock (box name + cgi-bin)  
> Fuzzed `/cgi-bin/` for `.sh`,`.py`, and other scripting extensions  
> Find `user.sh`  
> Use metasploit `/multi/http/apache_mod_cgi_bash_env_exec`
> Got User  
> Found `perl` NOPASSWD entry.  
> Root


### Analysis
There's no reason I should have looked at the writeup on this one, I'm a bit ashamed. I knew the Apache version and could see the needed exploit from EDB (using searchsploit). Based on the name of the box I figured it would require exploiting shellshock - but this was my first experience with shellshock.

#### Lessons Learned
> Go through each exploit and try to understand the exploit BEFORE using a walkthrough.



