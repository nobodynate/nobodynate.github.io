# Brainfuck

`Still in progress`

## Recon

The tags for [this box](https://app.hackthebox.com/machines/17) are:  
> - Cryptography

Difficulty:  
> Insane


NGINX is running on port 443 but could not access the website by IP.
After adding a name resolution to `/etc/hosts` I was able to access the site at `https://brainfuck.htb`. It's running WordPress 4.7.3, there is a login page at `/wp-admin`

One of the plugins is vulnerable
```bash
searchsploit ticket system 7.1.3                                         
```

![[Pasted image 20220115091350.png]]

EDB `41006`, `40939`
- These vulnerabilities require user-level access, so they aren't useful yet.

Nikto picked up an interesting link in the response headers:
```
+ Uncommon header 'link' found, with contents: <https://brainfuck.htb/?rest_route=/>; rel="https://api.w.org/"
```

Enumerating the API shows a bunch of different endpoints exposed.
One of the endpoints displays all users - the only user in this case is admin.

![[Pasted image 20220105072643.png]]

Maybe I can inject a user?
![[Pasted image 20220105073120.png]]

> NOTE - brainfuck (the name of this box) is also the name of an encoding algorithm on [this decoder](https://www.cachesleuth.com/multidecoder/). 
> Turns out this is a meme programming language. Read about it [on Wikipedia](https://en.wikipedia.org/wiki/Brainfuck)

At this point, it seems I should be looking for some brainfuck-encoded value and try to decode it, though after reading about brainfuck on wikipedia the author of this challenge likely put many rabbit-holes in place which will make it difficult to find the correct attack vector.

As I review scan results, I wonder if there is a passphrase associated with the TLS certificate. If I crack it, it may be the same pw for wordpress.

On the cert there is an AltName

![[Pasted image 20220115102857.png]]
I added the altname to `/etc/hosts`, for the same IP as `brainfuck.htb`. And sure enough there's a super secret hidden forum!

![[Pasted image 20220115103149.png]]

Also found a session cookie! Maybe this is the brainfuck-encoded value! Couldn't decode the cookie.

I was able to register an account.
Successful login looks like this:  
![[Pasted image 20220115112137.png]]

- There's another cookie named `flarum_remember`, which also doesn't decode to anything obvious.
- My created user has an ID of 4. Wonder who the other users are?

I was able to use forced browsing to find user with ID 3, which was the only mystery user (I already saw admin is 1 and restis is 2, I was 4)
![[Pasted image 20220115112350.png]]

Looking at the admin user, there appears to be some private posts and discussions:  
![[Pasted image 20220115111926.png]]

## Exploitation

Since I didn't find any other way to break the authentication mechanism, I decided to try a brute force attack. I decided to test the known usernames with a few wordlists. Since the usernames appear to follow a Greek Mythology theme, I will be using [this Greek wordlist]() to fuzz the 3 users.

![[Pasted image 20220115130509.png]]  
> User: `kostas`
> Pass: `123123123`

I logged in to the secret forum, but this user has nothing useful. The email provided for this user was kostas@testest.com - which makes me think this account is worthless. Of these accounts, the only one that also works in `/wp-admin/` is **admin**.

