"""O'zbek lotin matnini ovozga aylantirish (Meta MMS-TTS, kirill modeli).

Model: facebook/mms-tts-uzb-script_cyrillic  (litsenziya: CC-BY-NC 4.0, tijorat emas)
Ishlatish:
    python3 tts_uz.py "Matn" chiqish.wav
    yoki Python'dan:  from tts_uz import synth; synth("Matn", "out.wav")

Model faqat kirill harflarini biladi, shuning uchun lotin matn avval kirillga o'giriladi.
Raqamlarni so'z bilan yozing ("20" emas, "yigirma").
"""
import re, sys

MODEL = 'facebook/mms-tts-uzb-script_cyrillic'

_SIMPLE = {'a': 'а', 'b': 'б', 'c': 'с', 'd': 'д', 'f': 'ф', 'g': 'г', 'h': 'ҳ', 'i': 'и', 'j': 'ж', 'k': 'к',
           'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'q': 'қ', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у',
           'v': 'в', 'x': 'х', 'y': 'й', 'z': 'з'}
_VOWELS = set('aeiou')


def lat2cyr(text: str) -> str:
    t = text.lower()
    for ch in "’‘ʻʼ`´":
        t = t.replace(ch, "'")
    out, i, n = [], 0, len(t)
    while i < n:
        c, two = t[i], t[i:i + 2]
        word_start = i == 0 or not (t[i - 1].isalpha() or t[i - 1] == "'")
        if two in ("o'", "g'"):
            out.append('ў' if c == 'o' else 'ғ'); i += 2
        elif two == 'sh':
            out.append('ш'); i += 2
        elif two == 'ch':
            out.append('ч'); i += 2
        elif two == 'ng':
            out.append('нг'); i += 2
        elif two == 'yo':
            out.append('ё'); i += 2
        elif two == 'yu':
            out.append('ю'); i += 2
        elif two == 'ya':
            out.append('я'); i += 2
        elif two == 'ye':
            out.append('е'); i += 2
        elif c == 'e':
            out.append('э' if word_start else 'е'); i += 1
        elif c == "'":
            out.append('ъ' if i > 0 and t[i - 1].isalpha() else ''); i += 1
        elif c in _SIMPLE:
            out.append(_SIMPLE[c]); i += 1
        elif c in ' ,.?!-:;':
            out.append(c if c != '-' else ' '); i += 1
        else:
            i += 1  # noma'lum belgilar (↓, emoji) tashlab yuboriladi
    return re.sub(r'\s+', ' ', ''.join(out)).strip()


_model = _tok = None
_DEFAULTS = {}
PAUSE = {',': 0.22, ':': 0.30, ';': 0.30, '.': 0.40, '?': 0.45, '!': 0.40}


def _load():
    global _model, _tok
    from transformers import VitsModel, AutoTokenizer
    if _model is None:
        _model = VitsModel.from_pretrained(MODEL).eval()
        _tok = AutoTokenizer.from_pretrained(MODEL)
        _DEFAULTS.update(ns=_model.noise_scale, nsd=_model.noise_scale_duration)


def _clause_wave(cyr, seed):
    import torch
    ids = _tok(cyr, return_tensors='pt')
    torch.manual_seed(seed)
    with torch.no_grad():
        return _model(**ids).waveform[0].numpy()


def synth(text: str, path: str, speaking_rate: float = 1.0, seed: int = 555,
          noise_scale=None, noise_scale_duration=None, pauses: bool = True, chunk_words=None, chunk_pause=0.06, lowpass_hz=None):
    """Matnni ovozga aylantiradi.
    Model vocab'ida tinish belgilari yo'q (vergul, so'roq, nuqta, ikki nuqta tashlab yuboriladi), shuning uchun
    pauses=True bo'lsa matn tinish belgilari bo'yicha bo'laklarga bo'linadi, har bo'lak alohida o'qiladi va
    orasiga jimlik qo'yiladi (ritm va gap oxiri ohangi uchun)."""
    import numpy as np
    from scipy.io import wavfile
    _load()
    _model.speaking_rate = speaking_rate
    _model.noise_scale = _DEFAULTS['ns'] if noise_scale is None else noise_scale
    _model.noise_scale_duration = _DEFAULTS['nsd'] if noise_scale_duration is None else noise_scale_duration
    sr = _model.config.sampling_rate
    if pauses:
        parts = [p for p in re.split(r'([,.?!:;]+)', text) if p.strip()]
    else:
        parts = [text]
    pieces, last_clause = [], None
    for p in parts:
        if re.fullmatch(r'[,.?!:;]+', p.strip()):
            if last_clause is not None:
                pieces.append(np.zeros(int(sr * PAUSE.get(p.strip()[0], 0.25)), dtype=np.float32))
            continue
        words = p.split()
        n = chunk_words or len(words)
        subs = [' '.join(words[k:k + n]) for k in range(0, len(words), n)]
        for si, sub in enumerate(subs):
            cyr = lat2cyr(sub)
            if not cyr:
                continue
            w = _clause_wave(cyr, seed)
            w = w / max(1e-9, float(np.sqrt(np.mean(w ** 2)))) * 0.1   # har bo'lak bir xil ovoz balandligida
            if si > 0:
                pieces.append(np.zeros(int(sr * chunk_pause), dtype=np.float32))
            pieces.append(w); last_clause = cyr
    wav = np.concatenate(pieces)
    if lowpass_hz:  # yuqori chastotali shovqinni kesish (fine-tune model muallifi 7000 Hz tavsiya qiladi)
        import scipy.signal as sig
        b, a = sig.butter(2, lowpass_hz / (sr / 2), btype='low')
        wav = sig.filtfilt(b, a, wav).astype(np.float32)
    wav = wav / max(1e-9, np.abs(wav).max()) * 0.9
    wavfile.write(path, sr, (wav * 32767).astype(np.int16))
    return lat2cyr(text), len(wav) / sr


if __name__ == '__main__':
    cyr, dur = synth(sys.argv[1], sys.argv[2])
    print(cyr, f'({dur:.1f}s)')
