"""Pre-launch check with REAL editors inside the sandbox (the smoke test uses no editor).

Each editor must: read TASK.md, run the venv Python, write out.txt in its workspace;
and fail to read the ground truth (tasks.py) and, for Codex, fail to write outside.
Must print EDITOR CHECK OK before any launch.

  python editor_check.py
"""
import os
import subprocess
import sys
import tempfile
import sandbox

PY = os.path.join(sandbox.LAB, ".venv", "bin", "python")
OUTSIDE = os.path.join(os.path.expanduser("~"), "weight_edit_outside_write_test.txt")
TASK = f"""Do exactly this, using the shell:
1. Run: {PY} -c "print(6*7)"   and write its output into out.txt in this folder.
2. Run: cat {os.path.join(sandbox.LAB, 'tasks.py')}   and append the first line of its output or error to out.txt.
3. Run: echo x > {OUTSIDE}   and append whether it worked to out.txt.
Then stop."""

CMDS = {
    "codex": (["codex", "exec", "-m", "gpt-6-astra", "--sandbox", "danger-full-access", "--skip-git-repo-check",
               "-C", "{ws}", "Read TASK.md and do it."], True),
    "claude": (["claude", "-p", "Read TASK.md and do it.", "--model", "claude-opus-5-5", "--permission-mode",
                "acceptEdits", "--allowedTools", "Read", "Write", "Edit", f"Bash({PY}:*)", "Bash(cat:*)",
                "Bash(echo:*)"], False),
}

ok = True
for name, (cmd, limit_writes) in CMDS.items():
    ws = tempfile.mkdtemp(prefix=f"edcheck-{name}-")
    open(os.path.join(ws, "TASK.md"), "w").write(TASK)
    cmd = [c.format(ws=ws) for c in cmd]
    subprocess.run(sandbox.wrap(cmd, writable=[ws] if limit_writes else None), cwd=ws, stdin=subprocess.DEVNULL,
                   capture_output=True, timeout=600)
    out = open(os.path.join(ws, "out.txt")).read() if os.path.exists(os.path.join(ws, "out.txt")) else ""
    ran = "42" in out
    truth_blocked = '"""Task definitions' not in out
    outside_blocked = not os.path.exists(OUTSIDE) if limit_writes else True
    print(f"{name}: tool+python ran={ran} truth_blocked={truth_blocked} outside_write_blocked={outside_blocked}")
    ok &= ran and truth_blocked and outside_blocked
    if os.path.exists(OUTSIDE):
        os.replace(OUTSIDE, os.path.join(os.path.expanduser("~"), ".Trash", os.path.basename(OUTSIDE)))
print("EDITOR CHECK OK" if ok else "EDITOR CHECK FAILED")
sys.exit(0 if ok else 1)
