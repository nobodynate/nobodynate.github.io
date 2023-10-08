# Kotarak

`Still in progress`

## Recon

The tags on [this box](https://app.hackthebox.com/machines/101)  
> - Web
> - Arbitrary file upload

Difficulty:
> Hard

### Port Scan

```nmap

PORT      STATE SERVICE REASON         VERSION                                                                                                                       22/tcp    open  ssh     syn-ack ttl 63 OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)                                                                          8009/tcp  open  ajp13   syn-ack ttl 63 Apache Jserv (Protocol v1.3)                                                                                                          8080/tcp  open  http    syn-ack ttl 63 Apache Tomcat 8.5.5                                                                                                                   60000/tcp open  http    syn-ack ttl 63 Apache httpd 2.4.18 ((Ubuntu))                                                                                                                              Aggressive OS guesses: Linux 3.12 (95%), Linux 3.13 (95%), Linux 3.2 - 4.9 (95%), Linux 3.8 - 3.11 (95%), Linux 4.8 (95%), Linux 4.4 (95%), Linux 3.16 (95%), Linux 3.18 (95%), Linux 4.2 (95%), ASUS RT-N56U WAP (Linux 3.4) (95%)

```

Ssh seems to be up to date, and I've heard advice in the past about doing webservers last (since they can take the longest.) So we will start by examining Apache Jserv

## Apache Jserv (ajp v1.3)

According to [Hacktricks.xyz](https://book.hacktricks.xyz/pentesting/8009-pentesting-apache-jserv-protocol-ajp#cve-2020-1938-ghostcat)

> CVE-2020-1938 'Ghostcat'
> 
> If the AJP port is exposed, Tomcat might be susceptible to the Ghostcat vulnerability. Ghostcat is a LFI vulnerability, but somewhat restricted: only files from a certain path can be pulled. Still, this can include files like `WEB-INF/web.xml` which can leak important information like credentials for the Tomcat interface, depending on the server setup.


[EDB-48143](https://www.exploit-db.com/exploits/48143) is a public ghostcat exploit. I breifly reviewed the python script and it appears the variables are given as arguments; there's nothing in the script that needs to be modified. Running the script with no arguments gives the usage:

```bash
┌──(nate@kali-Dell)-[~/hackthebox/kotarak/exploit]                                                                                                                           └─$ ./48143.py                                                                                                                                                               usage: 48143.py [-h] [-p PORT] [-f FILE] target                                                                                                                              48143.py: error: too few arguments   
```

Now we need to define our arguments:
- PORT: AJP is running on port 8009
- FILE: good point, we'll have to find a file worth reading.
- target: the target is kotorak, which is at 10.10.10.55

### FInding potentially sensitive files.
Lets figure out what we can read with this.

Looking through some of the scan results, I notice the following directories of interest:
```
302        0l        0w        0c http://10.10.10.55:8080/docs
302        0l        0w        0c http://10.10.10.55:8080/examples
200       22l       93w    21630c http://10.10.10.55:8080/favicon.ico
302        0l        0w        0c http://10.10.10.55:8080/host-manager
200      202l      498w        0c http://10.10.10.55:8080/index.jsp
302        0l        0w        0c http://10.10.10.55:8080/manager
```

Now to scan each dir to see what files are in there.

I put all the directory URLs in a file called `urls` and will use this file to run multiple feroxbuster scans with some powershell kung-fu.

```powershell
cat ./urls | %{feroxbuster -u $_ -t 10 -w /usr/share/seclists/Discovery/Web-Content/big.txt -x "txt,html,php,asp,aspx,jsp" -v -k -n -q -o "/home/nate/hackthebox/kotarak/scans/tcp8080/tcp_8080_http_$($_.split('/')[3]).txt"}
```

