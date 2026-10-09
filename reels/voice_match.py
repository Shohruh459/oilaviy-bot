"""Ovoz fayl xususiyatlari (Praat/librosa): ohang balandligi va o'zgarishi, shimmer, jitter, RMS, davomiylik.

`chatterbox/select_voice_cb.py` shu yerdan `features()` ni ishlatadi. Shimmer ovoz "bo'g'ilganligi"ning ishonchli
ko'rsatkichi: yaxshi ~7-11%, bo'g'ilgan 14%+. DIQQAT: ovoz balandligini siljitmang (rubberband) va `loudnorm`
ishlatmang, shimmerni oshirib ovozni buzadi; faqat statik kuchaytirish.
"""
import numpy as np


def features(path):
    import librosa, parselmouth
    from parselmouth.praat import call
    y, sr = librosa.load(path, sr=16000)
    f0, _, _ = librosa.pyin(y, fmin=70, fmax=400, sr=sr)
    f0v = f0[~np.isnan(f0)]
    st = 12 * np.log2(f0v / 100.0)
    snd = parselmouth.Sound(path)
    pp = call(snd, 'To PointProcess (periodic, cc)', 70, 400)
    shim = call([snd, pp], 'Get shimmer (local)', 0, 0, 0.0001, 0.02, 1.3, 1.6) * 100
    jit = call(pp, 'Get jitter (local)', 0, 0, 0.0001, 0.02, 1.3) * 100
    return {'f0': float(np.median(st)), 'f0std': float(st.std()), 'dur': len(y) / sr,
            'shimmer': float(shim), 'jitter': float(jit), 'rms': float(np.sqrt(np.mean(y ** 2)))}
