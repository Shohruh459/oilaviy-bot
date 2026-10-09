import re, os, subprocess, sys
BASE='https://raw.githubusercontent.com/gokhaneraslan/chatterbox-finetuning/main/'
seen=set(); queue=['setup.py','src/config.py','src/model.py','src/utils.py','src/chatterbox_/tts.py','src/__init__.py','src/chatterbox_/__init__.py','merge_lora.py','inference.py','src/dataset.py','src/preprocess_ljspeech.py']
def fetch(p):
    os.makedirs(os.path.dirname(p) or '.',exist_ok=True)
    r=subprocess.run(['curl','-sS','-L','--max-time','30','-o',p,'-w','%{http_code}',BASE+p],capture_output=True,text=True)
    code=r.stdout.strip()
    if code!='200':
        if os.path.exists(p): os.remove(p)
        return None
    return open(p,encoding='utf-8',errors='replace').read()
def resolve(cur,mod,level):
    # returns candidate paths for a module
    if level==0: parts=mod.split('.')
    else:
        base=cur.split('/')[:-1]
        base=base[:len(base)-(level-1)] if level>1 else base
        parts=base+(mod.split('.') if mod else [])
    path='/'.join(parts)
    return [path+'.py', path+'/__init__.py']
while queue:
    p=queue.pop(0)
    if p in seen: continue
    seen.add(p)
    src=fetch(p)
    if src is None:
        print('404',p); continue
    print('OK ',p,len(src))
    if not p.endswith('.py'): continue
    for m in re.finditer(r'^\s*from\s+(\.*)([\w\.]*)\s+import\s+([\w, \(\)]+)',src,re.M):
        lvl=len(m.group(1)); mod=m.group(2)
        if lvl==0 and not (mod.startswith('src')): continue
        cands=resolve(p,mod,lvl)
        for c in cands: queue.append(c)
        # from pkg import submodule
        for name in re.split(r'[,\s\(\)]+',m.group(3)):
            if name and name[0].islower():
                for c in resolve(p,(mod+'.'+name) if mod else name,lvl): queue.append(c)
    for m in re.finditer(r'^\s*import\s+(src[\w\.]*)',src,re.M):
        queue.extend(resolve(p,m.group(1),0))
