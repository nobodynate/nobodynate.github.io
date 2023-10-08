# Hackpark

## Recon

The intro mentions

- **Brute Forcing** logins
- **Priv Esc** Windows
- **Ping is off**

## Scanning

Since ping is off, we will need to use the -Pn flag.
`nmap -PnV -T5 10.10.38.171`

![[afd75a6c2d9443f0b7c9beeab2f3c243.png]]

### Web Server :80

#### Browser

![[9fe2c03ef4844f40b8b92e9bbc27cfba.png]]

#### Whatweb scan

![[ffe70124ea124acda48998b70c4bb90d.png]]

#### Wappalyzer addon

![[c682663c9b224b60a34dcd2374bc3dca.png]]

### Plan

- [x] Need to find a login page
    **/admin**
- [x] Brute force login page to get greds
    **admin:1qaz2wsx**
- [x] Log in

After logging in, can view the framework/version
![[58d7942961964ba2968fb9f9999dcde7.png]]

`Searchsploit blogengine 3.3.6`
![[2f5a6e2adcfd44c1a7583a5a008a838f.png]]

`searchsploit -m 46353`
The found exploit uses **CVE-2019-6714**
Update line 51 with **IP** and **PORT** of listener on attack box.
![[1d3b5c8cc4904913aa8e8ecb9c470aa3.png]]
Next steps
![[01b3d393b67641ea8057824786a236ad.png]]
Initial Foothold
<img src=":/3e1cde9f3ecd460bba6414a2a334531b" alt="631008e8abf64d5f53fe51dbab2606ae.png" width="921" height="287">

## Enumeration

SystemInfo
![[30e289b93cb942eb90d4c4ecffae2220.png]]

Users
![[ec38dc36e63f454690bfeab2b1c79b42.png]]

## Exploit

Uploaded a **reverse meterpreter** using the same method as 46353.cs
![[3ccdd80cc9ed49598e2b7180622904e4.png]]
Set up a listener to catch the reverse meterpreter.
`msfconsole`
![[0b254712a5bb402982da74123b70fb64.png]]
`run`

Then back on the **iis apppool\\blog** shell, run the uploaded code.
Had to find the upload location
![[d66b62bc3b9a41a0aeec51e8455c2157.png]]
Navagate to the proper directory then run the code
![[22a39dc714794166a25822f2eb079513.png]]
![[c965b2d026b64fe98d67418b98f66c62.png]]
We got a reverse shell, though the user is still Blog.

![[d2781f7d2cda4a29930c8dbd20df47e9.png]]
![[c79050d28f934c3e9f0e7b44cf7455ad.png]]
WinPEAS seems to think we can use this autorun to run binaries. What's the file though...


user flag:
`759bd8af507517bcfaede78a21a73e39`

root flag:
`7e13d97f05f7ceb9881a3eb3d78d3e72`