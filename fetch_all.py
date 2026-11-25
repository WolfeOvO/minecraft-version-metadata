import json, hashlib, os, urllib.request, concurrent.futures, time

MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json"
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent":"wolfeovo-mcver-sync/1.0"})
    return urllib.request.urlopen(req, timeout=60).read()

os.makedirs("versions", exist_ok=True)
manifest = json.loads(get(MANIFEST_URL))
with open("version_manifest_v2.json","w") as f: json.dump(manifest,f,indent=2)
print("manifest saved,", len(manifest["versions"]), "versions")

def fetch_one(v):
    vid = v["id"]
    safe = vid.replace("/","_")
    path = f"versions/{safe}.json"
    if os.path.exists(path) and hashlib.sha1(open(path,'rb').read()).hexdigest() == v.get("sha1",""):
        return (vid, "skip")
    data = get(v["url"])
    with open(path,"wb") as f: f.write(data)
    return (vid, "ok")

results = []
with concurrent.futures.ThreadPoolExecutor(16) as ex:
    for r in ex.map(fetch_one, manifest["versions"]):
        results.append(r)
        if r[1]=="ok": pass
ok = sum(1 for _,s in results if s!="skip")
print("fetched:", ok, "skipped:", len(results)-ok)
