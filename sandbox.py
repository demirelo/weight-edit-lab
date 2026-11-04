"""Enforced boundary for editors (macOS sandbox-exec), applied to the editor process and
everything it starts.

Reads: ground truth, test data, earlier runs and review files are denied.
Writes (when `writable` is given): only the workspace and the tool's own state/temp dirs.
Codex cannot nest its own sandbox inside this one, so Codex runs with its sandbox off and
this profile is the only boundary.
"""
import os

LAB = os.path.abspath(os.path.dirname(__file__))
HOME = os.path.expanduser("~")
HIDDEN = os.path.join(HOME, ".weight-edit-hidden")
DENY_READ = [HIDDEN, os.path.join(LAB, "tasks.py"), os.path.join(LAB, "runs"), os.path.join(LAB, "laya", "runs"),
             os.path.join(LAB, "laya", "corrections.json"), os.path.join(LAB, "review"), os.path.join(LAB, "results")]
TOOL_STATE = [os.path.join(HOME, ".codex"), os.path.join(HOME, ".claude"), os.path.join(HOME, "Library", "Caches"),
              "/private/var/folders", "/dev"]


def wrap(cmd, writable=None):
    rules = "".join(f'(deny file-read* (subpath "{p}"))' for p in DENY_READ)
    if writable:
        allow = "".join(f'(subpath "{p}")' for p in [os.path.realpath(w) for w in writable] + TOOL_STATE)
        rules += f"(deny file-write*)(allow file-write* {allow})"
    return ["sandbox-exec", "-p", f"(version 1)(allow default){rules}"] + cmd
