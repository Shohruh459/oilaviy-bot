"""Ovozni bir xil qilish: har gapdan bir necha variant (seed) yaratib, namuna (reference) ovozga
balandligi, ohang o'zgarishi, tembri va tezligi eng yaqinini tanlaydi.

MMS-TTS (VITS) har safar biroz boshqacha ohang bilan o'qiydi, shuning uchun bir video ichida
gaplar turli ovozda chiqishi mumkin. Namuna: reels/voice_ref/ref_tavsiya.wav (foydalanuvchiga eng yoqqan gap).
Seed shimmer (ovoz sifati) va ohang bo'yicha namunaga eng yaqin tanlanadi; balandlik SILJITILMAYDI;
ovoz balandligi statik kuchaytirish bilan tenglanadi.
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
    import parselmouth
    from parselmouth.praat import call
    snd = parselmouth.Sound(path)
    pp = call(snd, 'To PointProcess (periodic, cc)', 70, 400)
    shim = call([snd, pp], 'Get shimmer (local)', 0, 0, 0.0001, 0.02, 1.3, 1.6) * 100
    jit = call(pp, 'Get jitter (local)', 0, 0, 0.0001, 0.02, 1.3) * 100
    rms = float(np.sqrt(np.mean(y ** 2)))
    return {'f0': float(np.median(st)), 'f0std': float(st.std()), 'cent': cent, 'mfcc': mf, 'dur': dur,
            'shimmer': float(shim), 'jitter': float(jit), 'rms': rms}


def distance(a, b):
    """Asosiy mezon: shimmer (ovoz tebranishining notekisligi; yuqori bo'lsa ovoz "bo'g'ilgan" eshitiladi).
    Qo'shimcha: ohang balandligi va o'zgarishi (kichik vazn). Tembr/mfcc hisobga olinmaydi (harflarga bog'liq)."""
    return (abs(a['shimmer'] - b['shimmer']) + 0.3 * abs(a['jitter'] - b['jitter'])
            + 0.4 * abs(a['f0'] - b['f0']) + 0.2 * abs(a['f0std'] - b['f0std']))


def _postprocess(src, dst, ref_rms=None):
    """Faqat statik kuchaytirish bilan ovoz balandligini namunaga tenglaydi.
    DIQQAT: balandlikni siljitish (rubberband) va loudnorm ishlatmang: shimmerni 2-5 punktga oshirib,
    ovozni "bo'g'ilgan" qiladi (foydalanuvchi shuni sezgan)."""
    import librosa, soundfile as sf
    y, sr = librosa.load(src, sr=16000)
    if ref_rms:
        y = y * (ref_rms / float(np.sqrt(np.mean(y ** 2))))
    peak = float(np.abs(y).max())
    if peak > 0.97:
        y = y * (0.97 / peak)
    sf.write(dst, y, sr)


def synth_matched(text, out_path, ref_wav, ref_text=None, seeds=range(1, 17), speaking_rate=1.1, verbose=True,
                  use_asr=False, **tts_kwargs):
    """Bir necha seed'dan sifati (shimmer) va ohangi namunaga eng yaqinini tanlaydi. Siljitish YO'Q.
    use_asr=True: har nomzod ASR (hear.py) bilan tekshiriladi va aniqroq o'qilgani (kam CER) afzal ko'riladi,
    lekin namuna ovozdan chiqib ketmaydi (shimmer <= namuna+1.2, ohang farqi <= 2 yarim ton).
    Qaytaradi: (seed, ball, yakuniy xususiyatlar; use_asr bo'lsa fin['cer'] ham)."""
    ref = features(ref_wav)
    best = None
    tmp = tempfile.mkdtemp()
    if use_asr:
        import hear
    for sd in seeds:
        p = os.path.join(tmp, f's{sd}.wav')
        tts_uz.synth(text, p, speaking_rate=speaking_rate, seed=sd, **tts_kwargs)
        f = features(p)
        d = distance(f, ref)
        cer = None
        score = d
        if use_asr:
            hyp, _, _ = hear.transcribe(p)
            cer = hear.cer(hear.norm(text), hear.norm(hyp))
            score = d + 10 * cer
            if f['shimmer'] > ref['shimmer'] + 1.2 or abs(f['f0'] - ref['f0']) > 2.0:
                score += 5
        if verbose:
            print(f'    seed {sd:>3}: masofa {d:.2f} shimmer {f["shimmer"]:.1f}' + (f' CER {cer*100:.0f}%' if cer is not None else ''))
        if best is None or score < best[0]:
            best = (score, sd, p, cer)
    score, sd, p, cer = best
    _postprocess(p, out_path, ref['rms'])
    final = features(out_path)
    final['cer'] = cer
    shutil.rmtree(tmp, ignore_errors=True)
    return sd, score, final
