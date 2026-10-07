#!/usr/bin/env python3
"""scenes.json + audio/vo_S*.wav -> build/timeline.json, subtitles/subtitles.srt, subtitles.ass.
Audio bo'lmasa sahna davomiyligi scenes.json'dagi 'dur' dan olinadi (PREVIEW rejimi).
Subtitr vaqtlari: jumla belgilari soniga proporsional (taxminiy). Haqiqiy audio bilan
aniq sinxron uchun forced alignment (masalan whisper/aeneas) kerak - README'ga qarang."""
import json, os, re, subprocess, sys
R = os.path.join(os.path.dirname(__file__), '..')
cfg = json.load(open(os.path.join(R, 'scripts/scenes.json')))
X, P0, P1 = cfg['xfade'], cfg['pad_start'], cfg['pad_end']
def alen(p):
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]).strip())
have_audio = True; t = 0.0; out = []
for i, s in enumerate(cfg['scenes']):
    ap = os.path.join(R, 'audio', f"vo_{s['id']}.wav")
    if os.path.exists(ap):
        al = alen(ap); dur = al + P0 + P1
    else:
        have_audio = False; al = s['dur'] - P0 - P1; dur = s['dur']; ap = None
    start = t
    out.append({**s, 'dur': round(dur, 3), 'start': round(start, 3), 'audio': ap, 'alen': round(al, 3)})
    t = start + dur - X
total = out[-1]['start'] + out[-1]['dur']
json.dump({'fps': cfg['fps'], 'xfade': X, 'total': round(total, 3), 'have_audio': have_audio, 'scenes': out},
          open(os.path.join(R, 'build/timeline.json'), 'w'), ensure_ascii=False, indent=1)
# --- subtitrlar
def ts(x, sep=','):
    h, m, sec = int(x // 3600), int(x % 3600 // 60), x % 60
    return f"{h:02d}:{m:02d}:{int(sec):02d}{sep}{int(round((sec % 1) * 1000)):03d}".replace('1000', '999')
def ts_ass(x):
    h, m, sec = int(x // 3600), int(x % 3600 // 60), x % 60
    return f"{h}:{m:02d}:{sec:05.2f}"
ev = []
for s in out:
    lines = s['subs']; w = [len(re.sub(r'\*', '', l)) for l in lines]; tot = sum(w)
    t0 = s['start'] + P0; span = s['alen']
    for l, n in zip(lines, w):
        d = span * n / tot
        ev.append((t0, t0 + d, l)); t0 += d
srt = ''
for k, (a, b, l) in enumerate(ev, 1):
    srt += f"{k}\n{ts(a)} --> {ts(b - 0.05)}\n{l.replace('*','')}\n\n"
open(os.path.join(R, 'subtitles/subtitles.srt'), 'w').write(srt)
hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Inter,64,&H00FFFFFF,&H00FFFFFF,&H00101010,&H80000000,-1,0,0,0,100,100,0,0,1,5,2,2,90,90,340,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
def ass_text(l):
    l = re.sub(r'\*(.+?)\*', r'{\\c&H66C7F2&}\1{\\c&HFFFFFF&}', l)  # oltin (BGR)
    return r"{\fad(180,180)\fscx92\fscy92\t(0,220,\fscx100\fscy100)}" + l
ass = hdr + ''.join(f"Dialogue: 0,{ts_ass(a)},{ts_ass(b-0.05)},Default,,0,0,0,,{ass_text(l)}\n" for a, b, l in ev)
open(os.path.join(R, 'subtitles/subtitles.ass'), 'w').write(ass)
# voiceover.txt
open(os.path.join(R, 'voiceover.txt'), 'w').write('\n\n'.join(f"[{s['id']}]\n{s['vo']}" for s in out) + '\n')
print(f"jami {total:.2f}s, audio={'bor' if have_audio else 'YO‘Q (preview)'}, {len(ev)} subtitr qatori")
