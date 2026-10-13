## Intro

This year's WWHF badge challenge is interesting. The badge has a few LEDs, 2 buttons, an LCD screen, a headphone jack, and a few other components. Given last year's badge challenge, I figured there was a high likihood that the badge designer would allow pulling firmware through USB like last year, so I decided to pack light.

## First glance

After getting the badge at registration, I tucked the badge in my bag and started networking (social, not TCP/IP). Later when I got to my room for the night, I pulled the badge out and decided to start hackin around.

## We can't hack here, this isn't bat country

Just like last year, the badge had no battery; you have to give it power over USB. I opted to plug it directly into my machine in an attempt to multi-task (I knew the firware would also likely be available).

The LCD screen read "WIFI connecting...."

I waited, and waited, and waited. My gut sank as I started to speculate that the badge's core functionality depended on an SSID that was only accessible at the con (or my unit was defective). I could wait for the con, or.....

## Firmware extraction

First, I had to figure out what my machine was seeing:
```bash
$ lsusb

Bus 003 Device 020: ID 303a:1001 Espressif USB JTAG/serial debug unit
```
After some Googling (or Gemini-ing) it was obvious that the contents of the chip could be dumped via `esptool`.

Given the dev nature of ESP boards, I took this as the layup it is.

## Strings - theory confirmed

The binary dump revealed many interesting things; there was what appeared to be an SSID "WWHF Badges" alongside what appeared to be a PSK "SuperRandomBadges1337@#JLKDLGF". Great! My device is not junk. The next logical step, given my distance from the legitimate AP, was to spin up a clone network to continue dynamic testing. However I didn't have a wifi router with me, and South Park sounded a lot more relaxing than `hostapd` at 11pm.

## Back burnin' and bull ridin'

Outside of bragging about the PSK discovery, I didn't do much more testing at the con. There were lots of people, and working on a CTF during a networking event felt like misdirected energy. There were mechanical bulls that needed to be ridden and Nerf guns that needed to be shot! I discussed the challenge with my collegue (who has ESP32 experience) and he speculated that the badge had to be sending WAV files to some LLM; there's no way a local model was running on the badge.

## Doomsday

After getting back to my home lab, I spun up a mock network with the same SSID and PSK to start digging in.

The first packet capture revealed that the device reaches out to `10.99.9.58:8000`. Easy enough, I set the network's address schema to match and configured a static IP for my dev machine. Running a simple HTTP Server on port 8000 revealed that the badge makes an HTTP request to `/ws` after the TCP handshake.

I started building a simple websockets server, and it hit me; no matter what I build out, the LLM and challenge logic are server-side at the con. I will not be able to complete the badge challenge from home!

## It ain't easy being cheaty

After some reverse engineering of the firmware, I discovered that the websocket messages were extrememly simple:

Once a WebSocket is established, the badge checks-in with the server:
  ```json
  {'type': 'hello', 'device': 'milehigh2026-voice', 'sr': 16000, 'fmt': 'pcm16', 'chunk_ms': 20, 'confirmed_flags': []}
  ```

Holding the PTT button on the badge sent a cluster of messages full of bytes. With claudes help I was able to add a feature to the server that stores the bytes as a .wav file. Success! I have a new wireless mic!

Apparently, if I had solved any of the challenges, the server would respond with a flag ID that my badge would store in `/flags.json`, resulting in one of the LEDs lighing up to broadcast my progress. My mock server could easily replicate this, and I'm now the proud owner of all 15 flags! This "completed" state turns the prestiege LED blue and the others orange if you were wondering.

## Waitin' on a blog

The badge has a url printed on the bottom: https://learning.antisyphontraining.com/pages/e-badge. The page currently says something about releasing a blog:

> After the conference, carbon-based lifeforms (BHIS staff) will use crude charcoal drawings (a blog post) to provide instructions on how to flash and set-up the badge for use at home. Break responsibly.

I'm excited for the blog, and greatful for the challenge. Hopefully they also release the server-side code so I can really solve the challenges fair and square! I suspect that some TTS engine running on my laptop fuzzing for prompt injections would have been the move, but we'll have to wait and see.