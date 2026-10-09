"""Yuksalish reels yig'ish skripti.

Ishlatish:  python3 -I build_reel.py spec.json
Ishchi papka (cwd) ichida kerak:  clips/<nom>.mp4 (to'liq HD klip), seg/, txt/, ov/ papkalari avtomatik yaratiladi.
spec.json namunasi: reels/specs/video2_diqqat.json
"""
import json, math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
GOLD = (255, 213, 79)
spec = json.load(open(sys.argv[1]))
for d in ('seg', 'txt', 'ov'):
    os.makedirs(d, exist_ok=True)
if os.environ.get('NOVOICE'):  # ovozsiz (faqat musiqa) variant
    for _sc in spec['scenes']:
        _sc.pop('voice', None)
    spec['cta'].pop('voice', None)

def audio_len(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                       capture_output=True, text=True, check=True)
    return float(r.stdout)

# Ovozli video: har sahna davomiyligi = ovoz uzunligi + kechikish + 0.9s (kamida "dur")
VOICE_DELAY = spec.get('voice_delay', 0.4)
for sc in spec['scenes']:
    if sc.get('voice'):
        sc['dur'] = round(max(sc.get('dur', 0), audio_len(sc['voice']) + VOICE_DELAY + 0.9), 2)

# ---------------- matnli sahnalar ----------------
def text_scene(i, sc):
    c, d, lines, top = sc['clip'], sc['dur'], sc['lines'], sc['top']
    xf = sc.get('xfrac', 0.5)
    f = ["scale=1080:1920:force_original_aspect_ratio=increase",
         f"crop=1080:1920:x=(iw-ow)*{xf}:y=0,fps=30,setsar=1"]
    ys, y = [], top + 45
    for t, s, col in lines:
        ys.append(y); y += int(s * 1.35)
    f.append(f"drawbox=x=0:y={top}:w=iw:h={y - top + 45}:color=black@0.58:t=fill")
    for j, ((t, s, col), yy) in enumerate(zip(lines, ys)):
        p = f'txt/{i}_{j}.txt'; open(p, 'w').write(t)
        f.append(f"drawtext=fontfile={FONT}:textfile={p}:fontsize={s}:fontcolor={col}:x=(w-text_w)/2:y={yy}:"
                 f"alpha='min(1,max(0,(t-{0.15 * j})/0.4))'")
    f += ["fade=t=in:d=0.3", f"fade=t=out:st={d - 0.3}:d=0.3", "format=yuv420p"]
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-stream_loop', '-1', '-ss', str(sc.get('start', 0.5)),
                    '-t', str(d), '-i', f"clips/{c}.mp4", '-vf', ",".join(f), '-an',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', f'seg/{i}.mp4'], check=True)

for i, sc in enumerate(spec['scenes']):
    text_scene(i, sc)

# ---------------- CTA: animatsiyali piktogrammalar ----------------
S = 4
def font(sz): return ImageFont.truetype(FONT, sz)

def glyph(kind, size):
    n = size * S
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0)); d = ImageDraw.Draw(im); k = n / 100
    if kind == 'save':
        d.polygon([(30*k, 18*k), (70*k, 18*k), (70*k, 84*k), (50*k, 66*k), (30*k, 84*k)], fill='white')
    elif kind == 'send':
        d.polygon([(16*k, 46*k), (86*k, 16*k), (60*k, 84*k), (46*k, 58*k)], fill='white')
        d.polygon([(46*k, 58*k), (86*k, 16*k), (50*k, 50*k)], fill=(0, 0, 0, 90))
    elif kind == 'follow':
        d.ellipse((24*k, 18*k, 56*k, 50*k), fill='white')
        d.pieslice((12*k, 52*k, 68*k, 108*k), 180, 360, fill='white')
        d.rectangle((72*k, 38*k, 80*k, 62*k), fill='white'); d.rectangle((64*k, 46*k, 88*k, 54*k), fill='white')
    return im.resize((size, size), Image.LANCZOS)

def instagram_icon(size):
    """Gradientli yumaloq kvadrat + oq kamera belgisi (tashqi logo fayl yo'q)."""
    n = size * S
    grad = Image.new('RGBA', (n, n))
    px = grad.load()
    stops = [(0.0, (254, 218, 117)), (0.35, (250, 126, 30)), (0.6, (214, 41, 118)), (0.85, (150, 47, 191)), (1.0, (79, 91, 213))]
    def col(t):
        for (a, ca), (b, cb) in zip(stops, stops[1:]):
            if a <= t <= b:
                u = (t - a) / (b - a); return tuple(int(ca[x] + (cb[x] - ca[x]) * u) for x in range(3)) + (255,)
        return stops[-1][1] + (255,)
    for y in range(n):
        for x in range(n):
            # diagonal: pastki-chapdan yuqori-o'ngga
            px[x, y] = col((x / n) * 0.45 + (1 - y / n) * 0.55)
    mask = Image.new('L', (n, n), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, n - 1, n - 1), radius=int(n * 0.26), fill=255)
    grad.putalpha(mask)
    d = ImageDraw.Draw(grad); k = n / 100; w = int(n * 0.065)
    d.rounded_rectangle((20*k, 20*k, 80*k, 80*k), radius=int(18*k), outline='white', width=w)
    d.ellipse((34*k, 34*k, 66*k, 66*k), outline='white', width=w)
    d.ellipse((66*k, 25*k, 74*k, 33*k), fill='white')
    return grad.resize((size, size), Image.LANCZOS)

def ease_back(t):
    if t <= 0: return 0
    if t >= 1: return 1
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

CATALOG = {'save': ("Saqlab qo'ying", "keyin kerak bo'ladi", (255, 193, 7)),
           'send': ("Do'stingizga", "yuboring", (33, 150, 243)),
           'follow': ("Obuna", "bo'ling", (76, 175, 80))}
cta = spec['cta']
order = cta.get('order', ['save', 'send', 'follow'])
ICONS = [(k,) + CATALOG[k] for k in order]
XS = [195, 540, 885]; CY = 1010; R = 118
FPS, DUR = 30, cta.get('dur', 5.5)
if cta.get('voice'):
    DUR = round(max(DUR, audio_len(cta['voice']) + VOICE_DELAY + 0.9), 2)
glyphs = [glyph(k, 130) for k, *_ in ICONS]
ig = instagram_icon(96)
brand = cta.get('brand', 'YUKSALISH')

def center_text(d, y, text, fnt, fill, cx=540):
    w = d.textlength(text, font=fnt); d.text((cx - w / 2, y), text, font=fnt, fill=fill)

for fr in range(int(FPS * DUR)):
    t = fr / FPS
    im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im, 'RGBA')
    a = min(1, t / 0.4)
    center_text(d, 560, cta.get('heading', "Foydali bo'ldimi?"), font(88), (255, 255, 255, int(255 * a)))
    center_text(d, 680, cta.get('sub', "Ilm yo'lida yuksalishda davom eting"), font(38), GOLD + (int(255 * a),))
    for n, ((kind, l1, l2, col), cx) in enumerate(zip(ICONS, XS)):
        t0 = 0.5 + 0.5 * n
        p = ease_back((t - t0) / 0.5)
        pulse = 1 + 0.04 * math.sin((t - t0 - 0.5) * 6) if t > t0 + 0.5 else 1
        sc = max(p, 0) * pulse
        if sc > 0:
            r = int(R * sc)
            d.ellipse((cx - r, CY - r, cx + r, CY + r), fill=col + (255,), outline=(255, 255, 255, 255), width=6)
            g = glyphs[n].resize((max(1, int(130 * sc)), max(1, int(130 * sc))), Image.LANCZOS)
            im.alpha_composite(g, (cx - g.width // 2, CY - g.height // 2))
            la = int(255 * min(1, max(0, (t - t0 - 0.3) / 0.3)))
            center_text(d, CY + 150, l1, font(40), (255, 255, 255, la), cx)
            center_text(d, CY + 200, l2, font(32), (230, 230, 230, la), cx)
    # brend qatori: [Instagram belgisi] YUKSALISH (yoki @nom)
    ba = min(1, max(0, (t - 2.2) / 0.5))
    fb = font(76); tw = d.textlength(brand, font=fb); gap = 22
    total = 96 + gap + tw; x0 = 540 - total / 2; yb = 1480
    ico = ig.copy(); ico.putalpha(ico.getchannel('A').point(lambda v: int(v * ba)))
    im.alpha_composite(ico, (int(x0), yb - 4))
    d.text((x0 + 96 + gap, yb), brand, font=fb, fill=GOLD + (int(255 * ba),))
    im.save(f'ov/{fr:03d}.png')

subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', '1', '-t', str(DUR), '-i', f"clips/{cta['bg']}.mp4",
                '-framerate', '30', '-i', 'ov/%03d.png', '-filter_complex',
                "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,"
                "boxblur=14:2,eq=brightness=-0.28[bg];[bg][1:v]overlay=format=auto,"
                f"fade=t=in:d=0.3,fade=t=out:st={DUR - 0.4}:d=0.4,format=yuv420p[v]",
                '-map', '[v]', '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', 'seg/cta.mp4'], check=True)

segs = [f'seg/{i}.mp4' for i in range(len(spec['scenes']))] + ['seg/cta.mp4']
open('list.txt', 'w').write("\n".join(f"file '{s}'" for s in segs))
total = sum(s['dur'] for s in spec['scenes']) + DUR
voices, t0 = [], 0.0
for sc in spec['scenes']:
    if sc.get('voice'):
        voices.append((sc['voice'], t0 + VOICE_DELAY))
    t0 += sc['dur']
if cta.get('voice'):
    voices.append((cta['voice'], t0 + VOICE_DELAY))

cmd = ['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-i', 'list.txt',
       '-ss', str(spec.get('music_start', 0)), '-i', spec['music']]
if not voices:
    cmd += ['-t', str(total), '-af', f'afade=t=in:d=1,afade=t=out:st={total - 3}:d=3', '-map', '0:v', '-map', '1:a']
else:
    for p, _ in voices:
        cmd += ['-i', p]
    parts, labels = [], []
    for k, (_, st) in enumerate(voices):
        parts.append(f"[{k + 2}:a]aresample=44100,adelay={int(st * 1000)}:all=1,volume={spec.get('voice_gain', 1.5)}[v{k}]")
        labels.append(f'[v{k}]')
    parts.append(("".join(labels) + f"amix=inputs={len(voices)}:normalize=0:dropout_transition=0[vo]") if len(voices) > 1
                 else "[v0]anull[vo]")
    parts.append(f"[1:a]aresample=44100,volume={spec.get('music_gain', 0.6)}[m]")
    parts.append("[vo]asplit[vk][vm]")
    parts.append("[m][vk]sidechaincompress=threshold=0.015:ratio=12:attack=30:release=700[md]")
    parts.append("[md][vm]amix=inputs=2:normalize=0:duration=longest[mix]")
    parts.append(f"[mix]atrim=0:{total},afade=t=in:d=1,afade=t=out:st={total - 3}:d=3,alimiter=limit=0.95,aformat=channel_layouts=stereo[a]")
    cmd += ['-filter_complex', ";".join(parts), '-map', '0:v', '-map', '[a]', '-t', str(total)]
cmd += ['-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', spec['out']]
subprocess.run(cmd, check=True)
print('total', total, '->', spec['out'])
