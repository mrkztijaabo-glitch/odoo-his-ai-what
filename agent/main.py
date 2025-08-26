import os, re, json, subprocess, textwrap, pathlib
from tenacity import retry, stop_after_attempt, wait_exponential
from github import Github
from openai import OpenAI

def run(cmd, cwd=None, check=True):
    print("+", cmd)
    r = subprocess.run(cmd, shell=True, cwd=cwd, text=True,
                       capture_output=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"{cmd}\n{r.stdout}\n{r.stderr}")
    return r.stdout

def collect_repo_context(max_chars=12000):
    """Collect a small slice of repo context to keep prompts fast."""
    globs = ["README.md", "pyproject.toml", "requirements.txt",
             "**/*.py", "**/*.xml", "**/*.js", "**/*.ts"]
    seen, buf = set(), []
    for pattern in globs:
        for p in pathlib.Path(".").rglob(pattern):
            if p.is_file() and p.suffix in {".md",".py",".xml",".js",".ts",".toml"}:
                if p.name.startswith(".") or p.as_posix() in seen:
                    continue
                seen.add(p.as_posix())
                try:
                    txt = p.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                snippet = txt[:2000]  # keep it light
                buf.append(f"\n=== {p.as_posix()} ===\n{snippet}")
                if sum(len(b) for b in buf) > max_chars:
                    return "\n".join(buf)
    return "\n".join(buf)

SYSTEM_PROMPT = """You are a careful software engineer.
Given a GitHub issue/comment describing a change, produce a single unified diff patch.
Rules:
- Output ONLY between the markers:
***BEGIN PATCH***
<unified diff>
***END PATCH***
- The diff must apply cleanly with `git apply --whitespace=fix`.
- Keep changes minimal; avoid unrelated edits.
"""

def build_user_prompt(issue_title, issue_body, comment_body, repo_context):
    return textwrap.dedent(f"""
    Task:
    - Issue title: {issue_title}
    - Issue body:\n{issue_body}
    - Trigger comment:\n{comment_body}

    Project context (truncated):
    {repo_context}

    Produce a unified diff patch for this repository.
    """)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def ask_openai(prompt, model="gpt-5.1-mini"):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    # Responses API (simple text output)
    resp = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    # Convenience property output_text is available; fall back if needed
    text = getattr(resp, "output_text", None)
    if not text:
        # Fallback extraction
        if resp.output and len(resp.output) and resp.output[0].content:
            text = "".join([c.get("text", {}).get("value", "") 
                            for c in resp.output[0].content if isinstance(c, dict)])
    return text or ""

def extract_patch(text):
    m = re.search(r"\*\*\*BEGIN PATCH\*\*\*(.+?)\*\*\*END PATCH\*\*\*", text, re.S)
    return m.group(1).strip() if m else ""

def create_branch(branch):
    run(f"git config user.name 'github-actions[bot]'")
    run(f"git config user.email '41898282+github-actions[bot]@users.noreply.github.com'")
    run(f"git checkout -b {branch}")

def apply_patch(patch):
    pathlib.Path("agent_out.patch").write_text(patch, encoding="utf-8")
    run("git apply --whitespace=fix agent_out.patch")
    run("git add -A")

def commit_and_push(branch, message):
    run(f"git commit -m {json.dumps(message)}")
    run(f"git push --set-upstream origin {branch}")

def open_pr(repo_full, head, base, title, body):
    gh = Github(os.environ.get("GITHUB_TOKEN"))
    repo = gh.get_repo(repo_full)
    pr = repo.create_pull(title=title, body=body, head=head, base=base)
    return pr.html_url

def main():
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        raise SystemExit("Run inside GitHub Actions.")
    event = json.loads(pathlib.Path(event_path).read_text())
    repo_full = os.environ["GITHUB_REPOSITORY"]
    default_branch = os.environ.get("GITHUB_REF_NAME", "main")

    issue = event["issue"]
    comment = event["comment"]

    if not comment["body"].strip().lower().startswith("/agent"):
        print("Comment does not start with /agent — exiting.")
        return

    repo_ctx = collect_repo_context()
    prompt = build_user_prompt(issue["title"], issue.get("body",""),
                               comment["body"], repo_ctx)
    raw = ask_openai(prompt)
    patch = extract_patch(raw)
    if not patch:
        raise RuntimeError("Model did not return a patch.")

    branch = f"agent/{issue['number']}-{comment['id']}"
    create_branch(branch)
    apply_patch(patch)
    commit_and_push(branch, f"agent: {issue['title']}")
    pr_url = open_pr(repo_full, branch, default_branch,
                     f"agent: {issue['title']}",
                     "Proposed by coding-agent 🤖")
    print("Opened PR:", pr_url)

if __name__ == "__main__":
    main()
