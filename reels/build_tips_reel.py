import json, math, os, subprocess
from PIL import Image, ImageDraw, ImageFont

F = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
MUSIC = '/root/.claude/uploads/67aa58e8-4a02-54d8-bf0f-942ba7352e6b/9cb7e78e-echoes_of_lumen-vlog-background-music-596303.mp3'
W, G, L = 'white', '0xFFD54F', '0xE6E6E6'
os.makedirs('seg', exist_ok=True); os.makedirs('txt', exist_ok=True); os.makedirs('ov', exist_ok=True)

meta = json.load(open('meta.json'))
need = ['hook_2', 'hook_3', 't2_3', 't3_3', 't4_3', 't5_3']
for n in need:
    fn = f'big_{n}.mp4'
    if not os.path.exists(fn):
        subprocess.run(['curl', '-sS', '-o', fn, meta[n + '.mp4']['large']], check=True)

# clip, dur, [(text, size, color)], box top
scenes = [
    ('big_hook_2', 3.5, [("Ko'p o'qiysiz-u,", 82, W), ("esda qolmayaptimi?", 82, W),
                         ("Ko'proq samara beradigan", 46, G), ("5 ta usul ↓", 46, G)], 1060),
    ('big_hook_3', 5, [("1-usul", 42, G), ("Kichik qadamlardan", 62, W), ("boshlang", 62, W),
                       ("Kuniga 20 daqiqa ham", 44, L), ("katta natija beradi", 44, L)], 1000),
    ('big_t2_3', 5, [("2-usul", 42, G), ("O'qiganingizni o'z", 62, W), ("so'zingiz bilan yozing", 62, W),
                     ("Mavzu shunda yaxshiroq", 44, L), ("esda qoladi", 44, L)], 1000),
    ('big_t3_3', 5, [("3-usul", 42, G), ("Takrorlashni", 62, W), ("oldindan rejalang", 62, W),
                     ("Ertasi kuni, 3 kundan so'ng", 44, L), ("va bir haftadan keyin", 44, L)], 1000),
    ('big_t4_3', 5, [("4-usul", 42, G), ("O'qish vaqtida", 62, W), ("telefonni chetga qo'ying", 58, W),
                     ("Diqqat jamlansa,", 44, L), ("tezroq o'rganasiz", 44, L)], 1000),
    ('big_t5_3', 5, [("5-usul", 42, G), ("Bilganingizni", 62, W), ("boshqalarga o'rgating", 62, W),
                     ("Mustahkamlashning eng", 44, L), ("yaxshi usullaridan biri", 44, L)], 1000),
]

XF = {'big_t3_3': 0.38, 'big_t4_3': 0.92}

def text_scene(i, c, d, lines, top):
    f = ["scale=1080:1920:force_original_aspect_ratio=increase",
         f"crop=1080:1920:x=(iw-ow)*{XF.get(c,0.5)}:y=0,fps=30,setsar=1"]
    ys = []; y = top + 45
    for t, s, col in lines:
        ys.append(y); y += int(s * 1.35)
    f.append(f"drawbox=x=0:y={top}:w=iw:h={y - top + 45}:color=black@0.58:t=fill")
    for j, ((t, s, col), yy) in enumerate(zip(lines, ys)):
        p = f'txt/{i}_{j}.txt'; open(p, 'w').write(t)
        f.append(f"drawtext=fontfile={F}:textfile={p}:fontsize={s}:fontcolor={col}:x=(w-text_w)/2:y={yy}:"
                 f"alpha='min(1,max(0,(t-{0.15 * j})/0.4))'")
    f += ["fade=t=in:d=0.3", f"fade=t=out:st={d - 0.3}:d=0.3", "format=yuv420p"]
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', '0.5', '-t', str(d), '-i', f'{c}.mp4', '-vf', ",".join(f),
                    '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', f'seg/{i}.mp4'], check=True)

for i, (c, d, lines, top) in enumerate(scenes):
    text_scene(i, c, d, lines, top)

# ---------- CTA scene: animated icons drawn with Pillow ----------
S = 4  # supersample
def font(sz): return ImageFont.truetype(F, sz)

def icon(kind, size):
    """white glyph on transparent canvas, size px (drawn 4x then downscaled)"""
    n = size * S
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    k = n / 100
    if kind == 'save':    # bookmark
        d.polygon([(30*k, 18*k), (70*k, 18*k), (70*k, 84*k), (50*k, 66*k), (30*k, 84*k)], fill='white')
    elif kind == 'send':  # paper plane
        d.polygon([(16*k, 46*k), (86*k, 16*k), (60*k, 84*k), (46*k, 58*k)], fill='white')
        d.polygon([(46*k, 58*k), (86*k, 16*k), (50*k, 50*k)], fill=(0, 0, 0, 90))
    elif kind == 'follow':  # person + plus
        d.ellipse((24*k, 18*k, 56*k, 50*k), fill='white')
        d.pieslice((12*k, 52*k, 68*k, 108*k), 180, 360, fill='white')
        d.rectangle((72*k, 38*k, 80*k, 62*k), fill='white'); d.rectangle((64*k, 46*k, 88*k, 54*k), fill='white')
    return im.resize((size, size), Image.LANCZOS)

def ease_back(t):
    if t <= 0: return 0
    if t >= 1: return 1
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

ICONS = [('save', 'Saqlab qo\'ying', 'keyin kerak bo\'ladi', (255, 193, 7)),
         ('send', 'Do\'stingizga', 'yuboring', (33, 150, 243)),
         ('follow', 'Obuna', 'bo\'ling', (76, 175, 80))]
XS = [195, 540, 885]; CY = 1010; R = 118
FPS, DUR = 30, 5.5
glyphs = [icon(k, 130) for k, *_ in ICONS]

def center_text(d, y, text, fnt, fill, cx=540):
    w = d.textlength(text, font=fnt); d.text((cx - w / 2, y), text, font=fnt, fill=fill)

for fr in range(int(FPS * DUR)):
    t = fr / FPS
    im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im, 'RGBA')
    a = min(1, t / 0.4)
    center_text(d, 560, "Foydali bo'ldimi?", font(88), (255, 255, 255, int(255 * a)))
    center_text(d, 680, "Ilm yo'lida yuksalishda davom eting", font(38), (255, 213, 79, int(255 * a)))
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
    center_text(d, 1480, "YUKSALISH", font(76), (255, 213, 79, int(255 * min(1, max(0, (t - 2.2) / 0.5)))))
    im.save(f'ov/{fr:03d}.png')

subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', '1', '-t', str(DUR), '-i', '../clips/e.mp4',
                '-framerate', '30', '-i', 'ov/%03d.png', '-filter_complex',
                "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,"
                "boxblur=14:2,eq=brightness=-0.28[bg];[bg][1:v]overlay=format=auto,"
                f"fade=t=in:d=0.3,fade=t=out:st={DUR - 0.4}:d=0.4,format=yuv420p[v]",
                '-map', '[v]', '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', 'seg/cta.mp4'], check=True)

segs = [f'seg/{i}.mp4' for i in range(len(scenes))] + ['seg/cta.mp4']
open('list.txt', 'w').write("\n".join(f"file '{s}'" for s in segs))
total = sum(s[1] for s in scenes) + DUR
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-i', 'list.txt', '-i', MUSIC, '-t', str(total),
                '-af', f'afade=t=in:d=1,afade=t=out:st={total - 3}:d=3', '-map', '0:v', '-map', '1:a',
                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart',
                'yuksalish_5_usul.mp4'], check=True)
print('total', total)
