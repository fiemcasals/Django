import urllib.request
import json
import subprocess

API_URL = "https://scrum.misitiowebpersonal.com.ar/api/v1"
API_KEY = "sk_593316cbe24b845d175d99ceaaf1b606d21bbe15ace000271258bc147d08632f"
REQ_ID = "REQ-1790272536899"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

def run(cmd):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"[{cmd}] -> {p.returncode}\nOUT: {p.stdout}\nERR: {p.stderr}")
    return p

print("=== 1. Setting REQ to doing ===")
patch_req = urllib.request.Request(f"{API_URL}/requirements/{REQ_ID}", data=json.dumps({"status": "doing"}).encode('utf-8'), headers=headers, method="PATCH")
with urllib.request.urlopen(patch_req) as resp:
    print(f"Status updated: {resp.status}")

print("=== 2. Requesting Branch Name from Scrum Master ===")
branch_name = None
try:
    branch_req = urllib.request.Request(
        f"{API_URL}/requirements/{REQ_ID}/github/branch",
        data=json.dumps({}).encode('utf-8'),
        headers=headers,
        method="POST"
    )
    with urllib.request.urlopen(branch_req) as resp:
        bdata = json.loads(resp.read().decode())
        branch_name = bdata.get("githubBranch")
        print(f"Assigned branch name: {branch_name}")
except Exception as e:
    print(f"Branch req note: {e}")

if not branch_name:
    branch_name = "feature/general/req-1790272536899-interfaz-web-y-chat-didactico"

print("=== 3. Updating local git repository ===")
run("git checkout dev")
run("git pull origin dev")
run(f"git checkout -b {branch_name}")
