#!/usr/bin/env python3
"""audio/vo_S1..S6.wav tekshiruvi: kanal, sample rate, davomiylik, clipping, jimlik. Xato bo'lsa exit 1."""
import json, os, re, subprocess, sys
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
D = os.environ.get('REELS_AUDIO', f'{R}/audio'); ids = [f'S{i}' for i in range(1, 7)]
files = {i: f'{D}/vo_{i}.wav' for i in ids}
present = [i for i in ids if os.path.exists(files[i])]
if not present: print('audio/ bo\'sh — tekshiruv o\'tkazib yuborildi (PREVIEW rejimi)'); sys.exit(0)
bad = [f'vo_{i}.wav YO\'Q' for i in ids if i not in present]
for i in present:
    p = files[i]; pr = json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','a:0','-show_entries',
        'stream=codec_name,channels,sample_rate,duration','-of','json',p]))['streams'][0]
    dur = float(pr.get('duration') or subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]))
    r = subprocess.run(['ffmpeg','-v','info','-i',p,'-af','astats=metadata=0:measure_perchannel=none,silencedetect=n=-50dB:d=0.4','-f','null','-'],
                       capture_output=True, text=True).stderr
    g = lambda k: [float(x) for x in re.findall(rf'{k}:\s*(-?[\d.inf]+)', r)]
    peak = max(g('Peak level dB') or [-99]); rms = (g('RMS level dB') or [-99])[-1]
    clipped = max(g('Number of clipped samples') or [0]) if 'Number of clipped samples' in r else 0
    sil = sum(float(x) for x in re.findall(r'silence_duration: ([\d.]+)', r))
    prob = []
    if dur < 0.8: prob.append('juda qisqa')
    if rms < -45: prob.append(f'deyarli jim (RMS {rms:.1f} dB)')
    if peak >= -0.1: prob.append(f'clipping xavfi (peak {peak:.2f} dBFS)')
    if sil > dur * 0.6: prob.append(f'ko\'p qismi jim ({sil:.1f}s)')
    ch = {1: 'mono', 2: 'stereo'}.get(pr['channels'], f"{pr['channels']}ch")
    print(f"vo_{i}.wav  {ch}  {pr['sample_rate']} Hz  {dur:5.2f}s  peak {peak:6.2f} dBFS  RMS {rms:6.1f} dB  silence {sil:.1f}s  {'OK' if not prob else 'XATO: ' + ', '.join(prob)}")
    if int(pr['sample_rate']) < 22050: prob.append('sample rate past')
    bad += [f'vo_{i}.wav: {x}' for x in prob]
if bad: print('\nMUAMMO:', *bad, sep='\n - '); sys.exit(1)
print('audio fayllar OK')
