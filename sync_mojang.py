#!/usr/bin/env python3
"""Incremental sync of Mojang official version metadata into this repo.
Downloads version_manifest_v2.json and every per-version JSON (by SHA1, idempotent).
Never downloads game jars - only metadata with official download URLs."""
import json, hashlib, os, urllib.request, concurrent.futures

MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json"
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent":"wolfeovo-mcver-sync/1.0"})
    return urllib.request.urlopen(req, timeout=60).read()

os.makedirs("versions", exist_ok=True)
manifest = json.loads(get(MANIFEST_URL))
with open("version_manifest_v2.json","w") as f: json.dump(manifest,f,indent=2)

def fetch_one(v):
    path = f"versions/{v['id'].replace('/','_')}.json"
    if os.path.exists(path) and hashlib.sha1(open(path,'rb').read()).hexdigest() == v.get("sha1",""):
        return False
    open(path,"wb").write(get(v["url"]))
    return True

with concurrent.futures.ThreadPoolExecutor(16) as ex:
    updated = sum(1 for r in ex.map(fetch_one, manifest["versions"]) if r)
print(f"versions={len(manifest['versions'])} updated={updated}")
