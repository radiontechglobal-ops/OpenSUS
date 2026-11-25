#!/usr/bin/env python3
"""Fail-closed preliminary lockfile gate; NOT a complete independence test."""
import json, pathlib, re, sys
root=pathlib.Path(__file__).resolve().parents[2]
blocked=re.compile(r'(?:^|[./@-])(?:github\.com|githubusercontent\.com|githubassets\.com|ghcr\.io|npmjs\.org|npmjs\.com|azure\.com|azureedge\.net|visualstudio\.com|microsoft\.com)(?:[/:?#.]|$)',re.I)
names=re.compile(r'^(typescript|tsgo|tslib|playwright(?:-core)?|@playwright/.*|@typescript/native-preview.*|@microsoft/.*|@azure/.*|@msal/.*)$',re.I)
findings=[]
for f in root.rglob('*lock.json'):
    if any(x in f.parts for x in ('node_modules','vendor','.git','artifacts')): continue
    if f.name!='package-lock.json': continue
    for path,p in json.loads(f.read_text())['packages'].items():
        if not path: continue
        name=path.split('node_modules/')[-1]
        if names.match(name) or blocked.search(p.get('resolved','')):
            findings.append({'file':str(f.relative_to(root)),'name':name,'version':p.get('version'),'url':p.get('resolved')})
for f in root.rglob('composer.lock'):
    if any(x in f.parts for x in ('node_modules','vendor','.git','artifacts')): continue
    data=json.loads(f.read_text())
    for p in data.get('packages',[])+data.get('packages-dev',[]):
        for field in ('source','dist'):
            url=(p.get(field) or {}).get('url','')
            if blocked.search(url): findings.append({'file':str(f.relative_to(root)),'name':p['name'],'version':p['version'],'field':field,'url':url})
out=root/'artifacts/independence/lock-gate.json'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps({'status':'FAIL' if findings else 'PARTIAL_PASS','findings':findings,'warning':'No runtime, ownership, installed component or network attestation'},indent=2)+'\n')
print(f'{len(findings)} findings; {out}')
sys.exit(1 if findings else 0)
