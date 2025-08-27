***BEGIN PATCH***
--- a/agent/main.py
+++ b/agent/main.py
@@
 SYSTEM_PROMPT = """You are a careful software engineer.
-Your only job is to produce a valid unified diff patch.
+Your ONLY output is a valid unified diff patch.
 
 Rules:
-- Output must be *only* between the markers:
+- Output must be ONLY between the markers:
 ***BEGIN PATCH***
 <unified diff>
 ***END PATCH***
-- No explanations, no prose, no notes outside the markers.
-- Patch must apply cleanly with `git apply --whitespace=fix`.
-- Always include proper file headers, e.g.:
-  --- path/to/file.py
-  +++ path/to/file.py
+- No explanations, no markdown fences.
+- The patch MUST include headers exactly like:
+  --- a/odoo_addons/his_core/models/patient.py
+  +++ b/odoo_addons/his_core/models/patient.py
+- Patch must apply with `git apply --whitespace=fix` (or `git apply -3`).
 - Keep the change minimal and relevant to the issue.
 """
@@
-def extract_patch(text):
-    m = re.search(r"\*\*\*BEGIN PATCH\*\*\*(.+?)\*\*\*END PATCH\*\*\*", text, re.S)
-    return m.group(1).strip() if m else ""
+def extract_patch(text: str) -> str:
+    """Extract patch between markers and strip accidental code fences."""
+    m = re.search(r"\*\*\*BEGIN PATCH\*\*\*(.+?)\*\*\*END PATCH\*\*\*", text, re.S)
+    if not m:
+        return ""
+    patch = m.group(1).strip()
+    # Remove accidental ```… fences
+    patch = re.sub(r"^```[^\n]*\n", "", patch)
+    patch = re.sub(r"\n```$", "", patch)
+    return patch
+
+def _first_path_from_comment(comment_body: str) -> str | None:
+    # Grab something like odoo_addons/.../.py from the comment
+    m = re.search(r"(odoo_addons/[A-Za-z0-9_/\.-]+\.py)", comment_body)
+    return m.group(1) if m else None
+
+def _generate_unified_diff(path: str, new_content: str) -> str:
+    """Create a valid unified diff from current file to new content."""
+    import difflib, io
+    a_path = f"a/{path}"
+    b_path = f"b/{path}"
+    try:
+        old = pathlib.Path(path).read_text(encoding="utf-8").splitlines(keepends=True)
+    except FileNotFoundError:
+        old = []
+    new = io.StringIO(new_content).read().splitlines(keepends=True)
+    diff = difflib.unified_diff(old, new, fromfile=a_path, tofile=b_path, lineterm="")
+    # Join and ensure trailing newline
+    out = "\n".join(diff)
+    if not out.endswith("\n"):
+        out += "\n"
+    return out
+
+def _looks_like_unified_diff(patch: str) -> bool:
+    return patch.startswith("--- ") and "\n+++ " in patch
@@
-def apply_patch(patch):
-    pathlib.Path("agent_out.patch").write_text(patch, encoding="utf-8")
-    run("git apply --whitespace=fix agent_out.patch")
-    run("git add -A")
+def apply_patch(patch: str):
+    # Save raw for debugging
+    pathlib.Path("agent_out.patch").write_text(patch, encoding="utf-8")
+    # If it isn't a proper diff, treat the text as new file content and build a diff
+    if not _looks_like_unified_diff(patch):
+        print("Model did not return a unified diff; attempting fallback…", flush=True)
+        # Try to infer target path from the comment
+        event = json.loads(pathlib.Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
+        comment_body = event.get("comment", {}).get("body", "")
+        target = _first_path_from_comment(comment_body)
+        if not target:
+            raise RuntimeError("Cannot infer target path from comment; patch was not a diff.")
+        # Build a proper unified diff
+        patch = _generate_unified_diff(target, patch)
+        pathlib.Path("agent_out.patch").write_text(patch, encoding="utf-8")
+        print("Fallback generated a unified diff.", flush=True)
+
+    # Basic sanity check: headers must exist
+    if "--- " not in patch or "+++ " not in patch:
+        raise RuntimeError("Generated patch looks invalid (missing ---/+++ headers):\n" + patch[:600])
+
+    # Try normal apply then 3-way merge
+    try:
+        run("git apply --whitespace=fix agent_out.patch")
+        run("git add -A")
+    except RuntimeError:
+        print("git apply failed, attempting 3-way merge (-3)…", flush=True)
+        run("git apply -3 --whitespace=fix agent_out.patch")
+        run("git add -A")
***END PATCH***
