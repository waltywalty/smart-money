import sys,json,base64,hashlib,subprocess,os
T=os.environ['GH_TOKEN']; REPO='waltywalty/smart-money'
def api(u):
    r=subprocess.run(['curl','-sS','-H','Authorization: Bearer '+T,'-H','Accept: application/vnd.github+json','-A','smart-money-kernel/1.0','-H','Expect:','--max-time','40','-w',chr(10)+'%{http_code}',u],capture_output=True,text=True)
    b,_,c=r.stdout.rpartition(chr(10)); return (int(c) if c.isdigit() else -1),b
for repo_path,local in [a.split('=') for a in sys.argv[1:]]:
    c,b=api('https://api.github.com/repos/%s/contents/%s?ref=main'%(REPO,repo_path))
    if c!=200: print('%-46s contents %d'%(repo_path,c)); continue
    sha=json.loads(b)['sha']
    c2,b2=api('https://api.github.com/repos/%s/git/blobs/%s'%(REPO,sha))
    raw=base64.b64decode(json.loads(b2)['content'])
    loc=open(local,'rb').read()
    h1=hashlib.sha256(raw).hexdigest(); h2=hashlib.sha256(loc).hexdigest()
    print('%-46s blob %d bytes  %s  %s'%(repo_path,len(raw),'IDENTICAL' if h1==h2 else 'MISMATCH',h1[:16]))
