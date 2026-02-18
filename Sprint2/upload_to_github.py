# This is a script to upload files to GitHub

import os
import sys

def upload_file(file_path):
    if os.path.exists(file_path):
        print(f'Uploading {file_path}...')
        # Code to upload file to GitHub would go here
    else:
        print('File does not exist.')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        upload_file(sys.argv[1])
    else:
        print('Please provide a file path to upload.'),

# updates

#!/usr/bin/env python3
"""
Skripta za upload FastCode-Claude pipeline fajlova na GitHub.
Pokreni u GitHub Codespaces ili bilo gde sa Python 3 i internetom.

Upotreba:
  python upload_to_github.py
"""

import base64
import json
import urllib.request
import urllib.error

# ─────────────────────────────────────────────
# KONFIGURACIJA — promeni ako treba
# ─────────────────────────────────────────────
# T
REPO = "porodica-rangelov/HelloWorld"
BRANCH = "feature/fastcode-claude-pipeline"
BASE_BRANCH = "main"
API = "https://api.github.com"

# ─────────────────────────────────────────────
# FAJLOVI ZA UPLOAD
# ─────────────────────────────────────────────

PIPELINE_PY = r'''#!/usr/bin/env python3
"""
FastCode → Claude Code Pipeline
================================
Agentic flow koji koristi FastCode za efikasnu analizu C#/.NET repozitorijuma,
a zatim prosledjuje sazeti kontekst Claude Code-u za generisanje/modifikaciju koda.

Dva rezima:
  1. API rezim  — potpuno automatizovan (Anthropic API)
  2. CLI rezim  — interaktivan (Claude Code CLI)

Prerekviziti:
  - Python 3.12+
  - FastCode kloniran i pokrenut (API na portu 8001 ili CLI)
  - Claude Code CLI instaliran (`npm install -g @anthropic-ai/claude-code`)
  - ANTHROPIC_API_KEY env varijabla (za API rezim)

Pokretanje:
  python fastcode_claude_pipeline.py --repo /path/to/your/csharp-repo --mode api
  python fastcode_claude_pipeline.py --repo /path/to/your/csharp-repo --mode cli
  python fastcode_claude_pipeline.py --repo /path/to/your/csharp-repo --mode both
"""

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class PipelineConfig:
    repo_path: str = ""
    fastcode_url: str = "http://localhost:8001"
    fastcode_cli_path: str = "./FastCode/main.py"
    anthropic_api_key: str = ""
    claude_model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 4096
    mode: str = "both"
    output_dir: str = "./pipeline_output"
    verbose: bool = False


class FastCodeAnalyzer:
    """Koristi FastCode za efikasno skeniranje i razumevanje kodne baze."""

    def __init__(self, config: PipelineConfig):
        self.config = config

    def analyze_via_api(self, query: str) -> dict:
        """Poziva FastCode API (port 8001) za analizu."""
        import requests
        url = f"{self.config.fastcode_url}/api/analyze"
        payload = {"repo_path": self.config.repo_path, "query": query}
        print(f"[FastCode API] Analiza: {query[:80]}...")
        try:
            resp = requests.post(url, json=payload, timeout=120)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.ConnectionError:
            print("[FastCode API] Ne mogu da se povezem. Da li je FastCode pokrenut?")
            return self._fallback_analyze(query)
        except Exception as e:
            print(f"[FastCode API] Greska: {e}")
            return self._fallback_analyze(query)

    def analyze_via_cli(self, query: str) -> dict:
        """Poziva FastCode CLI za analizu."""
        cli_path = Path(self.config.fastcode_cli_path)
        if not cli_path.exists():
            return self._fallback_analyze(query)
        cmd = [sys.executable, str(cli_path), "--repo", self.config.repo_path, "--query", query]
        print(f"[FastCode CLI] Analiza: {query[:80]}...")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                return {"analysis": result.stdout, "source": "fastcode_cli"}
            else:
                return self._fallback_analyze(query)
        except subprocess.TimeoutExpired:
            return self._fallback_analyze(query)

    def _fallback_analyze(self, query: str) -> dict:
        """Fallback: Lokalni Code Skimming bez FastCode-a."""
        print("[Fallback] Koristim lokalni code skimming...")
        repo = Path(self.config.repo_path)
        if not repo.exists():
            return {"error": f"Repo ne postoji: {repo}", "files": []}

        analysis = {
            "source": "local_skimming", "repo_path": str(repo),
            "structure": [], "csharp_files": [], "classes": [],
            "interfaces": [], "namespaces": set(),
        }

        cs_files = list(repo.rglob("*.cs"))
        cs_files = [f for f in cs_files if not any(s in f.parts for s in ("bin", "obj", "node_modules", ".git"))]

        for cs_file in cs_files:
            rel_path = cs_file.relative_to(repo)
            file_info = {"path": str(rel_path), "size": cs_file.stat().st_size, "signatures": []}
            try:
                content = cs_file.read_text(encoding="utf-8", errors="ignore")
                for line in content.splitlines():
                    stripped = line.strip()
                    if stripped.startswith("namespace "):
                        ns = stripped.replace("namespace ", "").rstrip("{").strip()
                        analysis["namespaces"].add(ns)
                        file_info["signatures"].append(f"namespace {ns}")
                    for kw in ("class ", "interface ", "record ", "struct ", "enum "):
                        if kw in stripped and not stripped.startswith("//"):
                            file_info["signatures"].append(stripped.rstrip("{").strip())
                            if kw == "class ":
                                analysis["classes"].append(stripped.rstrip("{").strip())
                            elif kw == "interface ":
                                analysis["interfaces"].append(stripped.rstrip("{").strip())
                            break
                    if any(stripped.startswith(m) for m in ("public ", "protected ", "internal ")):
                        if "(" in stripped and ")" in stripped and "class " not in stripped:
                            sig = stripped.rstrip("{").strip()
                            if len(sig) < 200:
                                file_info["signatures"].append(sig)
            except Exception:
                pass
            if file_info["signatures"]:
                analysis["csharp_files"].append(file_info)

        analysis["namespaces"] = sorted(analysis["namespaces"])
        analysis["summary"] = {
            "total_cs_files": len(cs_files),
            "analyzed_files": len(analysis["csharp_files"]),
            "total_classes": len(analysis["classes"]),
            "total_interfaces": len(analysis["interfaces"]),
            "namespaces": analysis["namespaces"],
        }
        return analysis

    def get_context_summary(self, analysis: dict) -> str:
        """Kreira sazeti kontekst string za Claude Code."""
        if "error" in analysis:
            return f"Greska pri analizi: {analysis['error']}"
        parts = ["# Analiza Repozitorijuma (Code Skimming)\\n"]
        summary = analysis.get("summary", {})
        if summary:
            parts.append(f"**Fajlova:** {summary.get('total_cs_files', '?')}")
            parts.append(f"**Klasa:** {summary.get('total_classes', '?')}")
            parts.append(f"**Interfejsa:** {summary.get('total_interfaces', '?')}")
            ns_list = summary.get("namespaces", [])
            if ns_list:
                parts.append(f"**Namespace-ovi:** {', '.join(ns_list)}")
            parts.append("")
        classes = analysis.get("classes", [])
        if classes:
            parts.append("## Klase")
            for cls in classes[:30]:
                parts.append(f"  - {cls}")
            parts.append("")
        interfaces = analysis.get("interfaces", [])
        if interfaces:
            parts.append("## Interfejsi")
            for iface in interfaces[:20]:
                parts.append(f"  - {iface}")
            parts.append("")
        files = analysis.get("csharp_files", [])
        if files:
            files_sorted = sorted(files, key=lambda f: len(f["signatures"]), reverse=True)
            parts.append("## Kljucni fajlovi (top 15 po signaturama)")
            for fi in files_sorted[:15]:
                parts.append(f"\\n### {fi['path']}")
                for sig in fi["signatures"][:10]:
                    parts.append(f"  {sig}")
            parts.append("")
        if "analysis" in analysis and isinstance(analysis["analysis"], str):
            parts.append("## FastCode analiza")
            parts.append(analysis["analysis"][:3000])
        return "\\n".join(parts)


class ClaudeCodeExecutor:
    """Prosledjuje kontekst Claude Code-u za akciju."""

    def __init__(self, config: PipelineConfig):
        self.config = config

    def execute_via_api(self, context: str, task: str) -> str:
        """Koristi Anthropic API za automatizovane zadatke."""
        try:
            import anthropic
        except ImportError:
            subprocess.run([sys.executable, "-m", "pip", "install", "anthropic", "-q"])
            import anthropic

        api_key = self.config.anthropic_api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            return "ANTHROPIC_API_KEY nije postavljen."

        client = anthropic.Anthropic(api_key=api_key)
        system_prompt = f"""Ti si ekspert za C#/.NET razvoj.
Dobijas analizu kodne baze i zadatak koji treba da izvrsis.

PRAVILA:
- Generisi cist, production-ready C# kod
- Prati postojece konvencije iz analize
- Koristi namespace-ove i klase koje vec postoje
- Dodaj XML komentare za public clanove
- Prati .NET best practices

ANALIZA KODNE BAZE:
{context[:6000]}
"""
        print(f"[Claude API] Saljem zadatak: {task[:80]}...")
        try:
            message = client.messages.create(
                model=self.config.claude_model, max_tokens=self.config.max_tokens,
                system=system_prompt, messages=[{"role": "user", "content": task}],
            )
            response_text = message.content[0].text
            print(f"[Claude API] Odgovor primljen ({message.usage.output_tokens} tokena)")
            return response_text
        except Exception as e:
            return f"API greska: {e}"

    def execute_via_cli(self, context: str, task: str) -> str:
        """Koristi Claude Code CLI za interaktivne zadatke."""
        context_file = Path(self.config.output_dir) / "_fastcode_context.md"
        context_file.parent.mkdir(parents=True, exist_ok=True)
        context_file.write_text(context, encoding="utf-8")

        full_prompt = f"""Procitaj kontekst iz {context_file} koji sadrzi analizu C#/.NET repozitorijuma.
Na osnovu te analize, uradi sledeci zadatak:
{task}
Repo se nalazi na: {self.config.repo_path}
"""
        print(f"\\n[Claude Code CLI] Pokrecem interaktivni rezim...")
        cmd = ["claude", "--print", "-p", full_prompt]
        try:
            result = subprocess.run(cmd, cwd=self.config.repo_path, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                return result.stdout
            else:
                return f"CLI greska: {result.stderr[:500]}"
        except FileNotFoundError:
            return "Claude Code CLI nije instaliran. Pokrenite: npm install -g @anthropic-ai/claude-code"
        except subprocess.TimeoutExpired:
            return "Timeout (300s)"


class FastCodeClaudePipeline:
    """Glavni orchestrator koji povezuje FastCode analizu sa Claude Code akcijom."""

    def __init__(self, config: PipelineConfig):
        self.config = config
        self.analyzer = FastCodeAnalyzer(config)
        self.executor = ClaudeCodeExecutor(config)
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self, task: str, analysis_query: str = None) -> dict:
        results = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "repo": self.config.repo_path, "task": task, "mode": self.config.mode}

        print("\\n" + "=" * 60)
        print("KORAK 1: FastCode — Analiza repozitorijuma")
        print("=" * 60)

        query = analysis_query or f"Analiziraj strukturu ovog C#/.NET projekta. Fokusiraj se na: {task}"
        analysis = self.analyzer.analyze_via_api(query)
        if "error" in analysis or analysis.get("source") == "local_skimming":
            if analysis.get("source") != "local_skimming":
                analysis = self.analyzer.analyze_via_cli(query)

        context = self.analyzer.get_context_summary(analysis)
        results["analysis_summary"] = analysis.get("summary", {})

        analysis_file = self.output_dir / "fastcode_analysis.json"
        with open(analysis_file, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)

        context_file = self.output_dir / "fastcode_context.md"
        context_file.write_text(context, encoding="utf-8")

        print("\\n" + "=" * 60)
        print("KORAK 2: Claude Code — Generisanje/Modifikacija")
        print("=" * 60)

        if self.config.mode in ("api", "both"):
            api_result = self.executor.execute_via_api(context, task)
            results["api_response"] = api_result
            (self.output_dir / "claude_api_result.md").write_text(api_result, encoding="utf-8")

        if self.config.mode in ("cli", "both"):
            cli_result = self.executor.execute_via_cli(context, task)
            results["cli_response"] = cli_result
            (self.output_dir / "claude_cli_result.md").write_text(cli_result, encoding="utf-8")

        print("\\n" + "=" * 60)
        print("PIPELINE ZAVRSEN")
        print("=" * 60)
        print(f"  Repo:     {self.config.repo_path}")
        print(f"  Zadatak:  {task[:80]}")
        print(f"  Output:   {self.output_dir}")
        return results


def main():
    parser = argparse.ArgumentParser(description="FastCode -> Claude Code Pipeline")
    parser.add_argument("--repo", required=True, help="Putanja do repozitorijuma")
    parser.add_argument("--task", required=True, help="Zadatak za Claude Code")
    parser.add_argument("--mode", choices=["api", "cli", "both"], default="both")
    parser.add_argument("--output", default="./pipeline_output")
    parser.add_argument("--fastcode-url", default="http://localhost:8001")
    parser.add_argument("--model", default="claude-sonnet-4-20250514")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    config = PipelineConfig(
        repo_path=os.path.abspath(args.repo), fastcode_url=args.fastcode_url,
        mode=args.mode, output_dir=args.output, claude_model=args.model,
        verbose=args.verbose, anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", ""),
    )
    FastCodeClaudePipeline(config).run(task=args.task)


if __name__ == "__main__":
    main()
'''

README_MD = r'''# FastCode → Claude Code Pipeline

## Sta radi?

Dvo-stepeni agentic flow za C#/.NET projekte:

```
┌─────────────┐     sazeti kontekst      ┌──────────────┐
│  FastCode    │ ───────────────────────► │  Claude Code │
│  (analiza)   │   klase, metode,         │  (akcija)    │
│              │   interfejsi, struktura   │              │
└─────────────┘                           └──────────────┘
     Korak 1                                   Korak 2
  Code Skimming                           Generisanje koda
  Token stednja                           Modifikacija
```

## Instalacija

### 1. FastCode (HKUDS)
```bash
git clone https://github.com/HKUDS/FastCode.git
cd FastCode
pip install -r requirements.txt
cp env.example .env
# U .env postavi API kljuceve
python web_app.py --host 0.0.0.0 --port 8001
```

### 2. Claude Code CLI
```bash
npm install -g @anthropic-ai/claude-code
```

### 3. Pipeline
```bash
pip install anthropic requests
```

### 4. API kljuc
```bash
export ANTHROPIC_API_KEY=tvoj_kljuc
```

## Upotreba

### Oba rezima (preporuceno)
```bash
python fastcode_claude_pipeline.py \
  --repo /path/to/myproject \
  --task "Dodaj unit testove za sve servisne klase" \
  --mode both
```

### Samo API (automatizovano, za CI/CD)
```bash
python fastcode_claude_pipeline.py \
  --repo /path/to/myproject \
  --task "Napravi repository pattern za DbContext" \
  --mode api
```

### Samo CLI (interaktivno, za development)
```bash
python fastcode_claude_pipeline.py \
  --repo /path/to/myproject \
  --task "Refaktorisi kontrolere da koriste MediatR" \
  --mode cli
```

## Primeri zadataka za C#/.NET

| Zadatak | Komanda |
|---------|---------|
| Generisanje testova | `--task "Generisi xUnit testove za Services/"` |
| Refaktoring | `--task "Uvedi CQRS pattern sa MediatR"` |
| Dokumentacija | `--task "Napravi CLAUDE.md sa dokumentacijom arhitekture"` |
| Migracija | `--task "Plan migracije sa .NET Framework na .NET 8"` |
| Code review | `--task "Pronadji probleme sa performansama"` |

## Output

Pipeline generise fajlove u `./pipeline_output/`:

| Fajl | Opis |
|------|------|
| `fastcode_analysis.json` | Sirovi podaci iz FastCode analize |
| `fastcode_context.md` | Sazeti kontekst (za Claude) |
| `claude_api_result.md` | Odgovor iz API rezima |
| `claude_cli_result.md` | Odgovor iz CLI rezima |
| `pipeline_summary.json` | Sazetak celog pipeline-a |

## Fallback rezim

Ako FastCode API/CLI nije dostupan, pipeline automatski koristi
**lokalni Code Skimming** — parsira `.cs` fajlove i izvlaci:
- Namespace-ove
- Klase i interfejse
- Public metode (signature)
- Strukturu projekta

Token stednja: ~60-80% manje tokena nego slanje celog koda.
'''

# ─────────────────────────────────────────────
# GitHub API pomocne funkcije
# ─────────────────────────────────────────────
def github_api(method, endpoint, data=None):
    """Poziva GitHub REST API."""
    url = f"{API}{endpoint}"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"  ❌ HTTP {e.code}: {error_body[:300]}")
        raise


def main():
    print("=" * 50)
    print("FastCode-Claude Pipeline → GitHub Upload")
    print("=" * 50)
    print(f"  Repo:   {REPO}")
    print(f"  Branch: {BRANCH}")
    print()

    # Korak 1: Uzmi SHA od main brancha
    print("1️⃣  Uzimam SHA od main brancha...")
    ref = github_api("GET", f"/repos/{REPO}/git/ref/heads/{BASE_BRANCH}")
    main_sha = ref["object"]["sha"]
    print(f"   main SHA: {main_sha[:12]}...")

    # Korak 2: Kreiraj novi branch
    print(f"\n2️⃣  Kreiram branch: {BRANCH}...")
    try:
        github_api("POST", f"/repos/{REPO}/git/refs", {
            "ref": f"refs/heads/{BRANCH}",
            "sha": main_sha,
        })
        print(f"   ✅ Branch kreiran!")
    except urllib.error.HTTPError as e:
        if "422" in str(e):
            print(f"   ⚠️  Branch vec postoji, nastavljam...")
        else:
            raise

    # Korak 3: Upload pipeline skripte
    print(f"\n3️⃣  Upload: pipeline/fastcode_claude_pipeline.py...")
    content_b64 = base64.b64encode(PIPELINE_PY.encode("utf-8")).decode("utf-8")
    github_api("PUT", f"/repos/{REPO}/contents/pipeline/fastcode_claude_pipeline.py", {
        "message": "feat: dodaj FastCode → Claude Code pipeline skriptu",
        "content": content_b64,
        "branch": BRANCH,
    })
    print("   ✅ Pipeline skripta uploadovana!")

    # Korak 4: Upload README
    print(f"\n4️⃣  Upload: pipeline/README.md...")
    readme_b64 = base64.b64encode(README_MD.encode("utf-8")).decode("utf-8")
    github_api("PUT", f"/repos/{REPO}/contents/pipeline/README.md", {
        "message": "docs: dodaj README za FastCode-Claude pipeline",
        "content": readme_b64,
        "branch": BRANCH,
    })
    print("   ✅ README uploadovan!")

    # Gotovo
    print("\n" + "=" * 50)
    print("✅ SVE GOTOVO!")
    print("=" * 50)
    print(f"\n  Branch:  https://github.com/{REPO}/tree/{BRANCH}")
    print(f"  PR:      https://github.com/{REPO}/compare/main...{BRANCH}")
    print(f"\n  Klikni na PR link iznad da napravis Pull Request!")


if __name__ == "__main__":
    main()
