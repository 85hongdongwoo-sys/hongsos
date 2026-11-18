import os,re,glob,shutil
root='preview'
shutil.rmtree(root,ignore_errors=True); shutil.copytree('site',root)
for x in ['CNAME','robots.txt','sitemap.xml']: os.remove(f'{root}/{x}')
for f in glob.glob(root+'/**/*.html',recursive=True):
    rel=os.path.relpath(os.path.dirname(f),root); depth=0 if rel=='.' else rel.count('/')+1
    pre='../'*depth or './'
    def fix(m):
        a,u=m.group(1),m.group(2).lstrip('/')
        u,_,h=u.partition('#'); h='#'+h if h else ''
        if u=='': u='index.html'
        elif u.endswith('/'): u+='index.html'
        return f'{a}="{pre}{u}{h}"'
    s=open(f).read().replace('<meta charset="utf-8">','<meta charset="utf-8">\n<meta name="robots" content="noindex,nofollow">',1)
    s=re.sub(r'(href|src)="(/[^"]*)"',fix,s)
    open(f,'w').write(s)
c=open(root+'/s.css').read().replace('url(/fonts/','url(fonts/'); open(root+'/s.css','w').write(c)
import json
fl=[{'as':os.path.relpath(p,root),'path':os.path.abspath(p)} for p in glob.glob(root+'/**/*',recursive=True) if os.path.isfile(p)]
json.dump(fl,open('files.json','w'));print(len(fl))
