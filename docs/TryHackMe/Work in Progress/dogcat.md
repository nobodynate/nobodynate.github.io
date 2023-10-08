# Dogcat

The only open ports on this one are SSH(22) and HTTP(80).

## Webserver

I was checking out the webserver and was able to trigger an error which seems to hint toward LFI vulnerability. My suspicion is based on this URL
`http://10.10.226.6/?view=dog../../../../etc/passwd`

Which produced this error on the webpage

> Warning: include(dog../../../../etc/passwd.php): failed to open stream: No such file or directory in /var/www/html/index.php on line 24
>
> Warning: include(): Failed opening 'dog../../../../etc/passwd.php' for inclusion (include_path='.:/usr/local/lib/php') in /var/www/html/index.php on line 24

I tried many methods to read `/etc/passwd` but was unsuccessful. Next step is to throw an LFI list using something like dirbuster or ZAP

