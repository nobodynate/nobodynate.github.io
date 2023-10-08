# Netmon

Port 21 (ftp) allows anonymous login, and we have read access to just about the whole system.

We see port 80 is open. it appears to be running PRTG Network Monitor.

There is an exploit available, however it requires creds.

We test default creds `prtgadmin:prtgadmin` but this is not a valid set of credentials. 

I did some searching online and found that the credentials (cleartext username and encrypted password) are stored in a configuration file at `C:\ProgramData\Paessler\PRTG Network Monitor\PRTG Configuration.dat`

We copy the file using FTP to inspect, and find the credentials we're after

![[Pasted image 20220714010256.png]]

```
JO3Y7LLK7IBKCMDN3DABSVAQO5MR5IDWF3MJLDOWSA======
```

```
OEASMEIE74Q5VXSPFJA2EEGBMEUEXFWW
```

We keep digging, and find that there is an unencrypted version of this password in the `old.bak` version of this file.
![[Pasted image 20220714011510.png]]

```
PrTg@dmin2019
```

It worked, and we're the System Administrator
![[Pasted image 20220714075200.png]]

EDB-46527 is supposed to work for PRTG but I was unable to get it to work. I found this article online that describes the exploit, and decided to try it manually: https://www.codewatch.org/blog/?p=453

To summarize, PRTG has a feature to execute a program when specific environmental conditionas occur within Network Monitor. The scripts must be added to the filesystem, and by desing there is no way to upload via the webapp. However, the PowerShell version of the demo script is vulnerable to command injection!

1. Go to **Setup > System Administration > Notifications** and click **Add new notification**
2. Turn on "Execute Program"
3. Select the .ps1 script
4. Apply the below parameter which will add a new user `pentest` with password `p3nT3st!`:
```
test.txt; net user pentest p3nT3st! /add
```
5. Save the notification
6. Run a test notification

Verify pwnage

![[Pasted image 20220714093330.png]]

Then use psexec to get a shell

```
psexec.py 'pentest:p3nT3st!'@netmon
```



