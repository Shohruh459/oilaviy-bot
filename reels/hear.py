"""Ovozni "eshitish": TTS natijasini ASR bilan matnga aylantirib tekshiradi.

1) ASR (Meta MMS-1b-all, uzb-script_latin adapteri): ovoz fayl nimani aytayotganini lotin harflarida yozadi.
   Aytilishi kerak matn bilan solishtirib, noto'g'ri o'qilgan so'zlarni topadi (CER = harf xatosi ulushi).
2) CTC forced alignment: har bir harf qancha davom etganini hisoblaydi (cho'zilgan/qisqargan harflar).
3) Speaker embedding (WavLM x-vector): gaplar bir odam ovoziga o'xshashligini kosinus o'xshashligi bilan o'lchaydi
   (model kartasidagi chegara ~0.86: undan past bo'lsa boshqa odam deb hisoblanadi).

Ishlatish:  python3 hear.py spec.json     (spec ichidagi "say" + "voice" fayllari tahlil qilinadi)
Litsenziya: facebook/mms-1b-all CC-BY-NC 4.0. Kerak: HF_HUB_DISABLE_XET=1, ~4 GB model.
"""
import difflib, json, os, re, sys
import numpy as np

os.environ.setdefault('HF_HUB_DISABLE_XET', '1')
import torch

ASR = 'facebook/mms-1b-all'
SV = 'microsoft/wavlm-base-plus-sv'
_asr = {}


def norm(text):
    """Taqqoslash uchun: kichik harf, barcha tutuq/apostrof variantlari bitta, tinish belgilarisiz."""
    t = text.lower()
    for ch in "’‘ʻʼ`´":
        t = t.replace(ch, "'")
    t = re.sub(r"[^a-z' ]+", " ", t.replace('ў', "o'").replace('ғ', "g'"))
    return re.sub(r'\s+', ' ', t).strip()


def load_asr():
    if not _asr:
        from transformers import Wav2Vec2ForCTC, AutoProcessor
        proc = AutoProcessor.from_pretrained(ASR, target_lang='uzb-script_latin')
        model = Wav2Vec2ForCTC.from_pretrained(ASR, target_lang='uzb-script_latin', ignore_mismatched_sizes=True).eval()
        _asr.update(proc=proc, model=model)
    return _asr['proc'], _asr['model']


def read_wav16k(path):
    import librosa
    y, _ = librosa.load(path, sr=16000)
    return y


def transcribe(path):
    proc, model = load_asr()
    y = read_wav16k(path)
    inp = proc(y, sampling_rate=16000, return_tensors='pt')
    with torch.no_grad():
        logits = model(**inp).logits[0]
    ids = logits.argmax(-1)
    text = proc.decode(ids)
    return text, logits.log_softmax(-1).numpy(), len(y) / 16000


def cer(ref, hyp):
    sm = difflib.SequenceMatcher(None, ref, hyp)
    same = sum(b.size for b in sm.get_matching_blocks())
    return 1 - same / max(1, len(ref))


def word_diff(ref, hyp):
    r, h = ref.split(), hyp.split()
    out = []
    sm = difflib.SequenceMatcher(None, r, h)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != 'equal':
            out.append(f"{' '.join(r[i1:i2]) or '-'} -> {' '.join(h[j1:j2]) or '-'}")
    return out


def ctc_align(logp, tokens, blank):
    """Oddiy CTC Viterbi forced alignment. Qaytaradi: har token uchun (boshlanish_kadr, tugash_kadr)."""
    T, L = logp.shape[0], len(tokens)
    S = 2 * L + 1
    ext = [blank] * S
    for i, t in enumerate(tokens):
        ext[2 * i + 1] = t
    NEG = -1e9
    dp = np.full((T, S), NEG); bp = np.zeros((T, S), dtype=np.int32)
    dp[0, 0] = logp[0, blank]
    if S > 1:
        dp[0, 1] = logp[0, ext[1]]
    for t in range(1, T):
        for s in range(S):
            best, arg = dp[t - 1, s], s
            if s >= 1 and dp[t - 1, s - 1] > best:
                best, arg = dp[t - 1, s - 1], s - 1
            if s >= 2 and ext[s] != blank and ext[s] != ext[s - 2] and dp[t - 1, s - 2] > best:
                best, arg = dp[t - 1, s - 2], s - 2
            dp[t, s] = best + logp[t, ext[s]]; bp[t, s] = arg
    s = S - 1 if dp[T - 1, S - 1] >= dp[T - 1, S - 2] else S - 2
    path = [0] * T
    for t in range(T - 1, -1, -1):
        path[t] = s; s = bp[t, s]
    spans = {}
    for t, s in enumerate(path):
        if s % 2 == 1:
            i = s // 2
            a, b = spans.get(i, (t, t)); spans[i] = (min(a, t), max(b, t))
    return [spans.get(i) for i in range(L)]


def char_durations(path, intended):
    proc, model = load_asr()
    text, logp, dur = transcribe(path)
    vocab = proc.tokenizer.get_vocab()
    blank = proc.tokenizer.pad_token_id
    chars = [c for c in norm(intended).replace(' ', '|') if c in vocab]
    tokens = [vocab[c] for c in chars]
    if logp.shape[0] < len(tokens) * 1:
        return text, dur, []
    spans = ctc_align(logp, tokens, blank)
    frame = dur / logp.shape[0]
    res = []
    for c, sp in zip(chars, spans):
        if sp is not None and c != '|':
            res.append((c, (sp[1] - sp[0] + 1) * frame))
    return text, dur, res


def speaker_similarity(paths):
    from transformers import AutoFeatureExtractor, WavLMForXVector
    fe = AutoFeatureExtractor.from_pretrained(SV)
    m = WavLMForXVector.from_pretrained(SV).eval()
    embs = []
    for p in paths:
        inp = fe(read_wav16k(p), sampling_rate=16000, return_tensors='pt')
        with torch.no_grad():
            e = m(**inp).embeddings[0]
        embs.append(torch.nn.functional.normalize(e, dim=-1))
    n = len(paths)
    return np.array([[float(embs[i] @ embs[j]) for j in range(n)] for i in range(n)])


if __name__ == '__main__':
    spec = json.load(open(sys.argv[1]))
    items = [(f'scene {i}', sc) for i, sc in enumerate(spec['scenes'])] + [('cta', spec['cta'])]
    items = [(n, it) for n, it in items if it.get('say') and it.get('voice') and os.path.exists(it['voice'])]
    print('\n== ASR: nima eshitildi (lotin harflari) ==')
    for name, it in items:
        text, _, _ = transcribe(it['voice'])
        ref, hyp = norm(it['say']), norm(text)
        print(f"{name}: kerak: {ref}\n{'':8}eshitildi: {hyp}\n{'':8}harf xatosi {cer(ref, hyp) * 100:.0f}% | farq: {word_diff(ref, hyp) or 'yo`q'}")
    print('\n== Ovoz egasi o\'xshashligi (kosinus; ~0.86+ bir odam) ==')
    paths = [it['voice'] for _, it in items]
    S = speaker_similarity(paths)
    names = [n for n, _ in items]
    print('        ' + ' '.join(f'{n[-3:]:>6}' for n in names))
    for i, n in enumerate(names):
        print(f'{n[-7:]:>8}' + ' '.join(f'{S[i, j]:6.2f}' for j in range(len(names))))
