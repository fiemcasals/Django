import json
import urllib.request
import urllib.error
import subprocess

PROJECT_ID = "PROJ-1790258465125"
REQ_ID = "REQ-1790272467589"
BRANCH = "feature/general/req-1790272467589-servicio-de-ia-con-anthropic-sdk-tool-ca"
SCRUM_BASE = "https://scrum.misitiowebpersonal.com.ar/api/v1"
SCRUM_TOKEN = "sk_593316cbe24b845d175d99ceaaf1b606d21bbe15ace000271258bc147d08632f"
HEADERS = {
    "Authorization": f"Bearer {SCRUM_TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_gh_token():
    proc = subprocess.run('git credential fill', input='protocol=https\nhost=github.com\n\n', text=True, capture_output=True, shell=True)
    for line in proc.stdout.splitlines():
        if line.startswith('password='):
            return line.split('password=', 1)[1].strip()
    raise Exception("Could not find GitHub token")

gh_token = get_gh_token()
gh_headers = {
    "Authorization": f"Bearer {gh_token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "Antigravity-Agent"
}

print("=== 1. Create/Update Pull Request on GitHub ===")
pr_payload = {
    "title": "feat(ia): Servicio de IA con Anthropic SDK, Tool Calling en 2 pasos y optimización de tokens (HU-04, RF-01)",
    "body": "Implementa Servicio de IA con Claude (Anthropic SDK) y patrón Tool Calling en 2 Fases:\n\n- `apps/ia/services.py`: `ClaudeService` con esquema liviano de Tools (`buscar_items_por_texto`, `filtrar_items_por_categoria`, `obtener_detalle_item`, `listar_catalogo_resumen`), ejecución local contra PostgreSQL vía ORM y síntesis final en segundo turno.\n- Manejo de excepciones de API (`AuthenticationError`, `RateLimitError`, `APIConnectionError`) sin elevar HTTP 500.\n- `apps/ia/tests/test_ai_service.py`: Suite completa de 4 tests unitarios con mocks.\n\nCloses REQ-1790272467589",
    "head": BRANCH,
    "base": "dev"
}
req = urllib.request.Request("https://api.github.com/repos/fiemcasals/Django/pulls", data=json.dumps(pr_payload).encode(), headers=gh_headers, method="POST")
try:
    with urllib.request.urlopen(req) as resp:
        pr_data = json.loads(resp.read().decode())
        pr_number = pr_data["number"]
        print(f"Created PR #{pr_number}")
except urllib.error.HTTPError as e:
    print(f"PR creation note: {e.read().decode()}")
    # Check existing PRs
    list_req = urllib.request.Request(f"https://api.github.com/repos/fiemcasals/Django/pulls?head=fiemcasals:{BRANCH}&state=open", headers=gh_headers)
    with urllib.request.urlopen(list_req) as lresp:
        prs = json.loads(lresp.read().decode())
        if prs:
            pr_number = prs[0]["number"]
            print(f"Found existing PR #{pr_number}")

print("=== 2. Transition Requirement to pr_open (Freeze Timer) ===")
patch_req = urllib.request.Request(f"{SCRUM_BASE}/requirements/{REQ_ID}", data=json.dumps({"status": "pr_open"}).encode(), headers=HEADERS, method="PATCH")
with urllib.request.urlopen(patch_req) as resp:
    print(f"Scrum requirement updated to pr_open: {resp.status}")

print("=== 3. Merge Pull Request into dev ===")
merge_payload = {
    "commit_title": f"Merge pull request #{pr_number} from {BRANCH}",
    "merge_method": "merge"
}
req = urllib.request.Request(f"https://api.github.com/repos/fiemcasals/Django/pulls/{pr_number}/merge", data=json.dumps(merge_payload).encode(), headers=gh_headers, method="PUT")
with urllib.request.urlopen(req) as resp:
    m_data = json.loads(resp.read().decode())
    print(f"Merged PR #{pr_number}: {m_data.get('message')}")
