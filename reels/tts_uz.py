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


def synth(text: str, path: str, speaking_rate: float = 1.0, seed: int = 555):
    global _model, _tok
    import torch, numpy as np
    from scipy.io import wavfile
    from transformers import VitsModel, AutoTokenizer
    if _model is None:
        _model = VitsModel.from_pretrained(MODEL).eval()
        _tok = AutoTokenizer.from_pretrained(MODEL)
    _model.speaking_rate = speaking_rate
    cyr = lat2cyr(text)
    ids = _tok(cyr, return_tensors='pt')
    torch.manual_seed(seed)
    with torch.no_grad():
        wav = _model(**ids).waveform[0].numpy()
    wav = wav / max(1e-9, np.abs(wav).max()) * 0.9
    wavfile.write(path, _model.config.sampling_rate, (wav * 32767).astype(np.int16))
    return cyr, len(wav) / _model.config.sampling_rate


if __name__ == '__main__':
    cyr, dur = synth(sys.argv[1], sys.argv[2])
    print(cyr, f'({dur:.1f}s)')
