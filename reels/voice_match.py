"""Ovozni bir xil qilish: har gapdan bir necha variant (seed) yaratib, namuna (reference) ovozga
balandligi, ohang o'zgarishi, tembri va tezligi eng yaqinini tanlaydi.

MMS-TTS (VITS) har safar biroz boshqacha ohang bilan o'qiydi, shuning uchun bir video ichida
gaplar turli ovozda chiqishi mumkin. Namuna: reels/voice_ref/ref_tavsiya.wav (foydalanuvchiga eng yoqqan gap).
Seed ohangi (pitch) namunaga eng yaqin tanlanadi, qolgan balandlik farqi rubberband bilan tenglanadi,
ovoz balandligi loudnorm bilan tenglanadi.
Eslatma: bu obyektiv akustik moslashtirish, men ovozni eshita olmayman, so'nggi hukm foydalanuvchiniki.
"""
import os, shutil, sys, tempfile
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tts_uz


def features(path):
    import librosa
    y, sr = librosa.load(path, sr=16000)
    f0, voiced, _ = librosa.pyin(y, fmin=70, fmax=400, sr=sr)
    f0v = f0[~np.isnan(f0)]
    st = 12 * np.log2(f0v / 100.0)
    cent = float(librosa.feature.spectral_centroid(y=y, sr=sr).mean())
    mf = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13).mean(axis=1)[1:]
    dur = len(y) / sr
    return {'f0': float(np.median(st)), 'f0std': float(st.std()), 'cent': cent, 'mfcc': mf, 'dur': dur}


def distance(a, b):
    """Faqat ohang (pitch) ko'rsatkichlari: harflar tarkibiga bog'liq tembr/tezlik hisobga olinmaydi."""
    return abs(a['f0'] - b['f0']) + abs(a['f0std'] - b['f0std'])


def _postprocess(src, dst, shift_st):
    """Balandlikni shift_st yarim tonga siljitadi (rubberband) va ovoz balandligini tenglaydi (loudnorm)."""
    import subprocess
    af = []
    if abs(shift_st) > 0.1:
        af.append(f"rubberband=pitch={2 ** (shift_st / 12):.5f}")
    af.append("loudnorm=I=-18:TP=-1.5:LRA=7")
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-af', ",".join(af), '-ar', '16000', '-ac', '1', dst], check=True)


def synth_matched(text, out_path, ref_wav, ref_text=None, seeds=range(1, 13), speaking_rate=1.1, verbose=True):
    """Bir necha seed'dan ohangi namunaga eng yaqinini tanlaydi, qolgan balandlik farqini siljitib tenglaydi.
    Qaytaradi: (seed, tanlashdagi masofa, yakuniy f0 farqi yarim tonda)."""
    ref = features(ref_wav)
    best = None
    tmp = tempfile.mkdtemp()
    for sd in seeds:
        p = os.path.join(tmp, f's{sd}.wav')
        tts_uz.synth(text, p, speaking_rate=speaking_rate, seed=sd)
        f = features(p)
        d = distance(f, ref)
        if verbose:
            print(f'    seed {sd:>3}: masofa {d:.2f}')
        if best is None or d < best[0]:
            best = (d, sd, p, f)
    d, sd, p, f = best
    _postprocess(p, out_path, ref['f0'] - f['f0'])
    final = features(out_path)
    shutil.rmtree(tmp, ignore_errors=True)
    return sd, d, final['f0'] - ref['f0']
