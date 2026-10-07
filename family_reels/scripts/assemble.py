#!/usr/bin/env python3
"""renders/S*.mp4 -> xfade -> subtitr (ASS) -> [audio mix + loudnorm] -> mp4.
Audio bor bo'lsa: final/family_happiness_reels.mp4. Yo'q bo'lsa: renders/preview_silent.mp4 (final EMAS)."""
import json, os, subprocess
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
tl = json.load(open(f'{R}/build/timeline.json')); X = tl['xfade']; sc = tl['scenes']; fps = tl['fps']
cmd = ['ffmpeg','-y','-v','error']
for s in sc: cmd += ['-i', f"{R}/renders/{s['id']}.mp4"]
f = ''; last = '0:v'
for i in range(1, len(sc)):
    off = sc[i]['start']
    f += f"[{last}][{i}:v]xfade=transition=fade:duration={X}:offset={off:.3f}[x{i}];"; last = f'x{i}'
T = tl['total']
f += (f"[{last}]fade=t=in:st=0:d=0.3,fade=t=out:st={T-0.7:.2f}:d=0.7,"
      f"ass={R}/subtitles/subtitles.ass:fontsdir=/usr/share/fonts[v]")
maps = ['-map','[v]']; out = f'{R}/renders/preview_silent.mp4'; aopts = ['-an']
if tl['have_audio']:
    k = len(sc)
    for s in sc: cmd += ['-i', s['audio']]
    af = ''
    for i, s in enumerate(sc):
        ms = int((s['start'] + 0.3) * 1000)
        af += f"[{k+i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[a{i}];"
    af += ''.join(f'[a{i}]' for i in range(k)) + f"amix=inputs={k}:normalize=0,apad,atrim=0:{T:.3f},"
    af += f"afade=t=out:st={T-0.6:.2f}:d=0.6,loudnorm=I=-16:TP=-1.5:LRA=11[a]"
    f += ';' + af; maps += ['-map','[a]']; out = f'{R}/final/family_happiness_reels.mp4'
    aopts = ['-c:a','aac','-b:a','192k','-ar','48000']
cmd += ['-filter_complex', f] + maps + ['-t', f'{T:.3f}', '-r', str(fps), '-c:v','libx264','-preset','slow','-crf','17',
        '-profile:v','high','-level','4.2','-pix_fmt','yuv420p','-movflags','+faststart'] + aopts + [out]
subprocess.run(cmd, check=True); print('tayyor:', out)
