# Breadcrumbs

`Still in progress`

## Recon

The tags on [this box](https://app.hackthebox.com/machines/316)  
> - Windows
> - SQL Injection
> - JSON
> - Source code review

Difficulty:
> Hard


### Port Scan

```text
22/tcp    open     ssh           syn-ack ttl 127                     OpenSSH for_Windows_7.7 (protocol 2.0)
135/tcp   open     msrpc         syn-ack ttl 127                     Microsoft Windows RPC
139/tcp   open     netbios-ssn   syn-ack ttl 127                     Microsoft Windows netbios-ssn
445/tcp   open     microsoft-ds? syn-ack ttl 127
3306/tcp  open     mysql?        syn-ack ttl 127
| mysql-info:
|_  MySQL Error: Host '10.10.16.3' is not allowed to connect to this MariaDB server
5040/tcp  open     unknown       syn-ack ttl 127
7680/tcp  open     pando-pub?    syn-ack ttl 127
30117/tcp filtered unknown       host-unreach from 10.10.16.1 ttl 64
49664/tcp open     msrpc         syn-ack ttl 127                     Microsoft Windows RPC
49665/tcp open     msrpc         syn-ack ttl 127                     Microsoft Windows RPC
49666/tcp open     msrpc         syn-ack ttl 127                     Microsoft Windows RPC
49667/tcp open     msrpc         syn-ack ttl 127                     Microsoft Windows RPC
49668/tcp open     msrpc         syn-ack ttl 127                     Microsoft Windows RPC
49669/tcp open     msrpc         syn-ack ttl 127                     Microsoft Windows RPC

Aggressive OS guesses:   
	Microsoft Windows 10 1709 - 1909 (95%),  
	Microsoft Windows Longhorn (94%),  
	Microsoft Windows 10 1703 (93%),  
	Microsoft Windows 7 SP1 (93%),  
	Microsoft Windows 8 (93%),  
	Microsoft Windows 10 1809 - 1909 (93%),  
	Microsoft Windows 10 1511 (92%),  
	Microsoft Windows Server 2008 R2 (92%),  
	Microsoft Windows Server 2008 SP2 (92%),  
	Microsoft Windows 8.1 Update 1 (92%)
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
```