#!/usr/bin/env python3
"""Microsoft Edge TTS (uz-UZ-SardorNeural / MadinaNeural) -> mp3. Ishlatish: tts_edge.py <voice> <matn> <chiqish.mp3> [rate]
Proksi muhitida CA bundle: /root/.ccr/ca-bundle.crt (TLS tekshiruvi O'CHIRILMAYDI)."""
import asyncio, os, sys, certifi
ca = os.environ.get('SSL_CERT_FILE') or '/root/.ccr/ca-bundle.crt'
if os.path.exists(ca): certifi.where = lambda: ca
import edge_tts
voice, text, out = sys.argv[1:4]; rate = sys.argv[4] if len(sys.argv) > 4 else '+0%'
asyncio.run(edge_tts.Communicate(text, voice, rate=rate).save(out))
