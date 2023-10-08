# Mirai

10.10.10.48

A port scan reveals ports 22 and 80 open.

Going to port 80 reveals this is a PiHole server. We can assume it's running on a raspberry pi and try the default credentials for ssh which are

> user: pi
> password: raspberry

This gets us a shell as the `pi` user. We always run `sudo -l` to see permissions once we get on the box, and to our suprise we can run everything. So we do `sudo su` and we are now ROOT.

## User Flag
We find the user flag
`/home/pi/Desktop/user.txt`

## Root Flag

However, the root flag `/root/root.txt` is not actually a flag. It just says the OG file went missing and to check the USB stick.

Using `df -h` we are able to see the usbstick mounted at `/media/usbstick`

We find `/media/usbstick/damnit.txt`, which says 

> Damnit! Sorry man I accidentally deleted your files off the USB stick.
Do you know if there is any way to get them back?
>
>-James

I tried a few things before turning to a walkthrough. It looks like the secret to getting the file is to
1. Clone the thumbdrive to a local file
```bash
sshpass -p raspberry ssh pi@10.10.10.48 "sudo dd if=/dev/sdb | gzip -1 -" | dd of=usb.gz
```
2. Extract the file
3. use `extundelete usb --restore-all` to recover all deleted files

Then, we find the root flag that was deleted.