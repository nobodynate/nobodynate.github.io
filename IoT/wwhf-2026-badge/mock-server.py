#!/usr/bin/env python3
"""Simple HTTP server on port 8000 that upgrades GET /ws to a WebSocket.

The badge sends a JSON "hello" (fmt=pcm16, chunk_ms=...) and then streams
mic audio as binary PCM16 frames while push-to-talk is held. Each burst of
binary frames (5-byte header + PCM16) is saved as a WAV file in ./recordings/.

Requires websockets 10.x (uses the process_request hook to serve plain HTTP).
"""
import argparse
import asyncio
import http
import json
import logging
import time
import wave
from pathlib import Path

import websockets

HOST = "0.0.0.0"
PORT = 8000
RECORDINGS_DIR = Path(__file__).parent / "recordings"
DEFAULT_SAMPLE_RATE = 16000  # used if it can't be inferred from chunk_ms
IDLE_FLUSH_SECONDS = 1.0     # save a WAV after this long without audio
FLAGS_TO_SEND = 0            # set by --flags

INDEX_HTML = b"""<!doctype html>
<html><head><meta charset="utf-8"><title>WS test</title></head>
<body>
<h1>WebSocket test</h1>
<input id="msg" value="hello"> <button onclick="ws.send(msg.value)">Send</button>
<pre id="log"></pre>
<script>
const log = (s) => document.getElementById('log').textContent += s + '\\n';
const ws = new WebSocket(`ws://${location.host}/ws`);
ws.onopen = () => log('[open]');
ws.onmessage = (e) => log('< ' + e.data);
ws.onclose = () => log('[closed]');
</script>
</body></html>
"""


async def process_request(path, request_headers):
    """Serve plain HTTP for everything except /ws, which proceeds to the WebSocket handshake."""
    if path == "/ws":
        return None
    if path == "/":
        return http.HTTPStatus.OK, [("Content-Type", "text/html; charset=utf-8")], INDEX_HTML
    return http.HTTPStatus.NOT_FOUND, [("Content-Type", "text/plain")], b"Not Found\n"


AUDIO_HEADER_LEN = 5  # 01 <seq u8> <utterance id u8> 00 00, then PCM16 LE mono


class AudioRecorder:
    """Collects binary audio frames (5-byte header + PCM16) and writes them out as mono WAV files."""

    def __init__(self, peer):
        self.peer = peer
        self.chunk_ms = None
        self.frames = []
        self.utterance = None
        self.last_seq = None

    def add(self, data: bytes):
        if len(data) < AUDIO_HEADER_LEN:
            logging.warning("short binary frame (%d bytes): %s", len(data), data.hex(" "))
            return
        header, pcm = data[:AUDIO_HEADER_LEN], data[AUDIO_HEADER_LEN:]
        kind, seq, utterance = header[0], header[1], header[2]
        if kind != 0x01 or header[3:] != b"\x00\x00":
            logging.warning("unexpected audio header: %s", header.hex(" "))
        if self.frames and utterance != self.utterance:
            self.flush()
        if not self.frames:
            logging.info("audio start: utterance=%d seq=%d frame=%d bytes", utterance, seq, len(data))
        elif self.last_seq is not None and seq != (self.last_seq + 1) % 256:
            logging.warning("seq gap: %d -> %d", self.last_seq, seq)
        self.utterance, self.last_seq = utterance, seq
        self.frames.append(pcm)

    def sample_rate(self):
        # Each frame holds chunk_ms of 16-bit mono audio: len = sr * chunk_ms/1000 * 2
        if self.chunk_ms and self.frames:
            return round(len(self.frames[0]) / 2 / (self.chunk_ms / 1000))
        return DEFAULT_SAMPLE_RATE

    def flush(self):
        if not self.frames:
            return
        RECORDINGS_DIR.mkdir(exist_ok=True)
        pcm = b"".join(self.frames)
        sr = self.sample_rate()
        path = RECORDINGS_DIR / f"{time.strftime('%Y%m%d-%H%M%S')}-{self.peer[0]}-u{self.utterance}.wav"
        with wave.open(str(path), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(sr)
            w.writeframes(pcm[: len(pcm) // 2 * 2])
        logging.info(
            "saved %s: %d frames, %d PCM bytes, sr=%d (%.2fs)",
            path.name, len(self.frames), len(pcm), sr, len(pcm) / 2 / sr,
        )
        self.frames = []
        self.last_seq = None


async def send_flags(websocket, confirmed):
    """Send flag_confirmed for flag1..flagN (the badge lights one LED per distinct flag id)."""
    if not FLAGS_TO_SEND:
        return
    logging.info("badge already has flags: %s", confirmed)
    for i in range(1, FLAGS_TO_SEND + 1):
        flag_id = f"flag{i}"
        logging.info("sending flag_confirmed id=%s", flag_id)
        await websocket.send(json.dumps({"type": "flag_confirmed", "flag_id": flag_id}))
        await asyncio.sleep(0.2)


async def ws_handler(websocket):
    peer = websocket.remote_address
    logging.info("WebSocket connected: %s", peer)
    rec = AudioRecorder(peer)
    try:
        while True:
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=IDLE_FLUSH_SECONDS)
            except asyncio.TimeoutError:
                rec.flush()
                continue

            if isinstance(message, bytes):
                rec.add(message)
                continue

            rec.flush()
            try:
                msg = json.loads(message)
            except json.JSONDecodeError:
                logging.info("text from %s: %r", peer, message)
                continue
            logging.info("json from %s: %s", peer, msg)
            if isinstance(msg, dict) and msg.get("type") == "hello":
                rec.chunk_ms = msg.get("chunk_ms")
                await websocket.send(json.dumps({
                    "type": "display", "line1": "connected", "line2": "", "line3": "", "line4": "",
                }))
                await send_flags(websocket, msg.get("confirmed_flags") or [])
    except websockets.ConnectionClosed:
        pass
    finally:
        rec.flush()
        logging.info("WebSocket disconnected: %s", peer)


async def main():
    async with websockets.serve(ws_handler, HOST, PORT, process_request=process_request):
        logging.info("Listening on http://%s:%d (WebSocket at /ws)", HOST, PORT)
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--flags", type=int, default=0, choices=range(0, 16), metavar="N",
                        help="on connect, send flag_confirmed for flag1..flagN to light N LEDs (0-5, default 0)")
    FLAGS_TO_SEND = parser.parse_args().flags
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    asyncio.run(main())
