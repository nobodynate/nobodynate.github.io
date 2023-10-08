# Devel

10.10.10.5

ports 21 and 80 are open

FTP allows anonymous access

we can upload
![[Pasted image 20220718121015.png]]


I upload an aspx webshell and have command execution.

We then ran sherlock


```
Title      : ClientCopyImage Win32k                                                                           
MSBulletin : MS15-051                                                                                         
CVEID      : 2015-1701, 2015-2433                                                                             
Link       : https://www.exploit-db.com/exploits/37367/                                                       
VulnStatus : Appears Vulnerable 

Title      : Task Scheduler .XML                                                                              
MSBulletin : MS10-092                                                                                         
CVEID      : 2010-3338, 2010-3888                                                                             
Link       : https://www.exploit-db.com/exploits/19930/                                                       
VulnStatus : Appears Vulnerable

Title      : User Mode to Ring (KiTrap0D)                                                                     
MSBulletin : MS10-015                                                                                         
CVEID      : 2010-0232                                                                                        
Link       : https://www.exploit-db.com/exploits/11199/                                                       
VulnStatus : Appears Vulnerable
```

I tried each of these, with no success.
Then I used google for `Windows 7 Enterprise Privilege escallation` and the first result is `MS11-046`. I found a precompiled binary here: https://github.com/abatchy17/WindowsExploits/tree/master/MS11-046

Using the shell we got from msfvenom I am able to run the exploit and get system admin.

![[Pasted image 20220718140738.png]]
