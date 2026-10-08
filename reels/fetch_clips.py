import os, json, subprocess, urllib.parse
key = os.environ['PIXABAY_API_KEY']
Q = {'hook': 'confused student thinking', 't1': 'clock time study', 't2': 'writing notes notebook',
     't3': 'calendar planning schedule', 't4': 'phone put away focus', 't5': 'teaching explaining friends'}
meta = {}
for k, q in Q.items():
    url = 'https://pixabay.com/api/videos/?' + urllib.parse.urlencode(
        {'key': key, 'q': q, 'per_page': 4, 'safesearch': 'true'})
    d = json.loads(subprocess.run(['curl', '-sS', url], capture_output=True, text=True, check=True).stdout)
    for n, h in enumerate(d['hits'][:4]):
        v = h['videos']
        src = next(v[s] for s in ('small', 'medium', 'tiny', 'large') if v[s]['url'])
        fn = f'{k}_{n}.mp4'
        subprocess.run(['curl', '-sS', '-o', fn, src['url']], check=True)
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', '2', '-i', fn, '-frames:v', '1',
                        '-vf', 'scale=-1:300', f'{k}_{n}.png'], check=True)
        meta[fn] = {'id': h['id'], 'dur': h['duration'], 'large': v['large']['url'],
                    'w': v['large']['width'], 'h': v['large']['height']}
json.dump(meta, open('meta.json', 'w'), indent=1)
rows = []
for k in Q:
    subprocess.run(['ffmpeg', '-y', '-v', 'error'] + sum([['-i', f'{k}_{n}.png'] for n in range(4)], []) +
                   ['-filter_complex', 'hstack=4', f'row_{k}.png'], check=True)
    rows.append(f'row_{k}.png')
subprocess.run(['ffmpeg', '-y', '-v', 'error'] + sum([['-i', r] for r in rows], []) +
               ['-filter_complex', 'vstack=6', 'grid.png'], check=True)
print('ok')
