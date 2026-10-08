#!/usr/bin/env python3
"""renders/S*.mp4 -> xfade -> subtitr (ASS) -> [audio mix + loudnorm] -> mp4.
Audio bor bo'lsa: build/candidate.mp4 (render.sh QC dan o'tgach final/ ga ko'chiradi). Yo'q bo'lsa: renders/preview_silent.mp4 (final EMAS)."""
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
maps = ['-map','[v]']; out = os.environ.get('REELS_OUT') or f'{R}/renders/preview_silent.mp4'; aopts = ['-an']
if tl['have_audio']:
    k = len(sc)
    for s in sc: cmd += ['-i', s['audio']]
    af = ''
    for i, s in enumerate(sc):
        ms = int((s['start'] + 0.3) * 1000)
        af += f"[{k+i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[a{i}];"
    af += ''.join(f'[a{i}]' for i in range(k)) + f"amix=inputs={k}:normalize=0,apad,atrim=0:{T:.3f},afade=t=out:st={T-0.6:.2f}:d=0.6"
    # 2 o'tishli loudnorm: avval o'lchaymiz, so'ng linear rejimda aniq -16 LUFS / TP -1.5 dB
    mcmd = ['ffmpeg','-y','-v','info'] + [x for s_ in sc for x in ['-i', s_['audio']]]
    pre = ''.join(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int((sc[i]['start']+0.3)*1000)}|{int((sc[i]['start']+0.3)*1000)}[a{i}];" for i in range(k))
    mcmd += ['-filter_complex', pre + ''.join(f'[a{i}]' for i in range(k)) + f"amix=inputs={k}:normalize=0,apad,atrim=0:{T:.3f},afade=t=out:st={T-0.6:.2f}:d=0.6,loudnorm=I=-16:TP=-2:LRA=11:print_format=json", '-f','null','-']
    r = subprocess.run(mcmd, capture_output=True, text=True)
    m = json.loads(r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}')+1])
    print('o\'lchov:', {x: m[x] for x in ('input_i','input_tp','input_lra')})
    af += (f",loudnorm=I=-16:TP=-2:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
           f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,alimiter=limit=0.84:level=false[a]")
    f += ';' + af; maps += ['-map','[a]']; out = os.environ.get('REELS_OUT') or f'{R}/build/candidate.mp4'
    aopts = ['-c:a','aac','-b:a','192k','-ar','48000']
cmd += ['-filter_complex', f] + maps + ['-t', f'{T:.3f}', '-r', str(fps), '-c:v','libx264','-preset','slow','-crf','17',
        '-profile:v','high','-level','4.2','-pix_fmt','yuv420p','-movflags','+faststart'] + aopts + [out]
subprocess.run(cmd, check=True); print('tayyor:', out)
