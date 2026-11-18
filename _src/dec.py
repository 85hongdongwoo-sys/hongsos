import json,base64,re,sys
from PIL import Image
f,names=sys.argv[1],sys.argv[2].split(',')
t=json.load(open(f))[0]['text']
m=re.match(r'"([A-Za-z0-9+/=#]+)"',t)
assert m, t[-150:]
for n,p in zip(names,m.group(1).split('#####')):
    open(f'img/{n}.jpg','wb').write(base64.b64decode(p))
    im=Image.open(f'img/{n}.jpg').convert('RGB'); im.save(f'img/{n}.jpg',quality=76,optimize=True,progressive=True); print(n,im.size)
