Shout out to **cäesura**, here is the writeup as promised! I'll add to it if we ever figure out the final answer.

Quiz 7 contains 2 parts

part 1
```text
⠢⠖⠲⠶⠖⠦⠖⠉⠲⠔⠲⠦⠲⠆⠖⠦⠖⠒⠒⠒⠲⠑⠒⠒⠖⠆⠒⠒⠲⠁⠖⠃⠲⠔⠲⠶⠲⠖⠶⠢⠢⠁⠲⠒⠲⠆⠲⠁⠢⠖⠖⠔⠲⠆⠖⠦⠖⠒⠖⠙⠢⠢⠖⠶⠲⠔⠖⠑⠲⠆⠖⠦⠖⠒⠒⠒⠲⠑⠒⠒⠖⠆⠒⠒⠲⠁⠖⠃⠖⠒⠲⠶⠲⠖⠶⠁⠖⠒⠒⠒⠖⠲⠶⠖⠖⠒⠖⠙⠢⠂⠖⠔
```

and part 2
```text
..-. ----- ..--- -.-. ...-- ---.. ..... ---.. ----- ...-- .- ..--- ..... -... ..-. --... -.-. ..--- ..--- --... ..-. ...-- .---- -.... .- -.-. . -.. .---- ---.. .---- ....- --... ----. -.-. -.. ...-- ..-. ----. ----- ...-- -... ---.. -.... -.. . ...-- . -... -.... ...-- -.. .- ----- -.. -.-. . . .- ..--- ..-. --... -.. .----
```

For this quiz we will be using [Cyber Chef](https://gchq.github.io/CyberChef/), which is a great resource for chaining together different ciphers or encodings in real time.

## Part 1
### Challenge

The challenge is to decode this:
```text
⠢⠖⠲⠶⠖⠦⠖⠉⠲⠔⠲⠦⠲⠆⠖⠦⠖⠒⠒⠒⠲⠑⠒⠒⠖⠆⠒⠒⠲⠁⠖⠃⠲⠔⠲⠶⠲⠖⠶⠢⠢⠁⠲⠒⠲⠆⠲⠁⠢⠖⠖⠔⠲⠆⠖⠦⠖⠒⠖⠙⠢⠢⠖⠶⠲⠔⠖⠑⠲⠆⠖⠦⠖⠒⠒⠒⠲⠑⠒⠒⠖⠆⠒⠒⠲⠁⠖⠃⠖⠒⠲⠶⠲⠖⠶⠁⠖⠒⠒⠒⠖⠲⠶⠖⠖⠒⠖⠙⠢⠂⠖⠔
```

The characters look familiar, and I just happened to remember that this is braille. Cyber Chef was able to make easy work of converting the braille to ASCII characters with the `From Braille` ingredient.

```text
5647686C4948426863334E3362334A6B494746755A43424A56694268636D5567496E426863334E3362334A6B6347467A63336476636D5169
```

The ASCII output (above) doesn't immediately look familiar. However, after looking at it for a few minutes I realized the character set matches up with Hexidecimal; this is just poorly formatted with no delimeter. We add the `From Hex` ingredient to our recipe and set the Delimeter to `None`.

![[Pasted image 20220626202033.png]]

Our output is now:
```text
VGhlIHBhc3N3b3JkIGFuZCBJViBhcmUgInBhc3N3b3JkcGFzc3dvcmQi
```

This resembles base 64 encoding, so lets try that out in the recipe, and VOILA! A cake.

![[Pasted image 20220626202216.png]]

### Answer

Our answer to part 1 is

> The password and IV are "passwordpassword"

## Part 2

### Challenge

```text
..-. ----- ..--- -.-. ...-- ---.. ..... ---.. ----- ...-- .- ..--- ..... -... ..-. --... -.-. ..--- ..--- --... ..-. ...-- .---- -.... .- -.-. . -.. .---- ---.. .---- ....- --... ----. -.-. -.. ...-- ..-. ----. ----- ...-- -... ---.. -.... -.. . ...-- . -... -.... ...-- -.. .- ----- -.. -.-. . . .- ..--- ..-. --... -.. .----
```

This part is incomplete, but at first glance I noticed the charset seemed to match written morse code. The dots are "shorts" and lines are "longs". The space is a delim between characters.

![[Pasted image 20220626203126.png]]

### Incomplete answer
> F02C385803A25BF7C227F316ACED181479CD3F903B86DE3EB63DA0DCEEA2F7D1

So, we decoded to this string, and have a `password and IV` which are both `passwordpassword`. If we were able to identify which cipher was used we would be able to decode this string further. Until then!